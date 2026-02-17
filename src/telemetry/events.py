from __future__ import annotations
import json
import os
import time
from pathlib import Path

ENABLED = os.getenv("SERAPHIS_TELEMETRY_ENABLED", "false").lower() == "true"
LOG_PATH = Path(os.getenv("SERAPHIS_TELEMETRY_LOG", "telemetry.log"))


def emit(event_type: str, payload: dict) -> None:
    if not ENABLED:
        return
    record = {"ts": time.time(), "event_type": event_type, "payload": payload}
    LOG_PATH.write_text(LOG_PATH.read_text() + json.dumps(record) + "\n" if LOG_PATH.exists() else json.dumps(record) + "\n")


def improvement_hints(stats: dict) -> list[str]:
    hints = []
    if stats.get("avg_latency_ms", 0) > 250:
        hints.append("Consider caching and payload compaction for slow endpoints")
    if stats.get("error_rate", 0) > 0.05:
        hints.append("High error rate detected; inspect policy denies and validation")
    if stats.get("payload_bytes_p95", 0) > 100_000:
        hints.append("Large payloads observed; enable compression")
    return hints
