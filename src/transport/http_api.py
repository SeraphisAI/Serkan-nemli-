from __future__ import annotations
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from core.models import SensorReading, UpdateApplyRequest
from core.service import SensorService
from policy.evaluator import PolicyEvaluator
from privacy.controls import mask_payload
from quantum.simulator import LocalQuantumSimulator, QuantumJob
from telemetry.events import emit, improvement_hints
from update.channel import apply_update, check_update


class AppState:
    def __init__(self) -> None:
        self.service = SensorService()
        self.policy = PolicyEvaluator()
        self.quantum = LocalQuantumSimulator()


state = AppState()


from security.auth import is_valid_api_key

def _authorized(headers: dict) -> bool:
    return is_valid_api_key(headers.get("x-api-key", ""))


def handle_request(method: str, path: str, headers: dict, body: dict | None = None) -> tuple[int, dict]:
    body = body or {}
    if method == "GET" and path == "/health":
        return 200, {"status": "ok", "version": "0.1.0"}
    if method == "POST" and path == "/v1/sensors/ingest":
        if not _authorized(headers):
            return 401, {"detail": "invalid api key"}
        start = time.perf_counter()
        allowed, reason = state.policy.evaluate("ingest", headers.get("x-role", "operator"))
        emit("policy", {"action": "ingest", "allow": allowed, "reason": reason})
        if not allowed:
            return 403, {"accepted": False, "reason": reason}
        reading = SensorReading(**body)
        result = state.service.ingest(reading)
        emit("request", mask_payload(reading.model_dump()))
        emit("latency", {"endpoint": path, "ms": (time.perf_counter() - start) * 1000})
        return 200, result
    if method == "GET" and path == "/v1/sensors/summary":
        return 200, state.service.summary()
    if method == "POST" and path == "/v1/quantum/run":
        job = QuantumJob(**body)
        return 200, {"result": state.quantum.run(job)}
    if method == "GET" and path == "/update/check":
        return 200, check_update()
    if method == "POST" and path == "/update/apply":
        if not _authorized(headers):
            return 401, {"detail": "invalid api key"}
        allowed, reason = state.policy.evaluate("update_apply", headers.get("x-role", "operator"))
        emit("policy", {"action": "update_apply", "allow": allowed, "reason": reason})
        if not allowed:
            return 403, {"applied": False, "reason": reason}
        req = UpdateApplyRequest(**body)
        return 200, apply_update(req)
    if method == "GET" and path == "/telemetry/hints":
        sample = {"avg_latency_ms": 300, "error_rate": 0.07, "payload_bytes_p95": 210000}
        return 200, {"hints": improvement_hints(sample)}
    return 404, {"detail": "not found"}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        status, payload = handle_request("GET", self.path, {k.lower(): v for k, v in self.headers.items()})
        self._send(status, payload)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        body = json.loads(raw.decode() or "{}")
        status, payload = handle_request("POST", self.path, {k.lower(): v for k, v in self.headers.items()}, body)
        self._send(status, payload)


def serve(host: str = "0.0.0.0", port: int = 8080) -> None:
    HTTPServer((host, port), Handler).serve_forever()
