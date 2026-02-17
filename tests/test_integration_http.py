import hashlib
import hmac
import os

from transport.http_api import handle_request


def test_health_and_ingest_flow():
    os.environ["SERAPHIS_API_KEY"] = "dev-secret-key"
    status, body = handle_request("GET", "/health", {})
    assert status == 200
    assert body["status"] == "ok"

    payload = {"sensor_id": "s1", "ts": 1700000000, "temperature_c": 21.5, "humidity_pct": 40.0, "location": "lab"}
    status, body = handle_request(
        "POST",
        "/v1/sensors/ingest",
        {"x-api-key": "dev-secret-key", "x-role": "operator"},
        payload,
    )
    assert status == 200
    assert body["accepted"] is True


def test_update_apply_requires_admin_and_valid_signature():
    os.environ["SERAPHIS_API_KEY"] = "dev-secret-key"
    os.environ["SERAPHIS_UPDATE_HMAC_KEY"] = "dev-hmac-key"
    sha = "abc123"
    sig = hmac.new(b"dev-hmac-key", sha.encode(), hashlib.sha256).hexdigest()
    req = {"package": {"version": "0.1.1", "notes": "patch", "payload_sha256": sha, "signature": sig}, "approver": "alice"}
    status, deny = handle_request("POST", "/update/apply", {"x-api-key": "dev-secret-key", "x-role": "operator"}, req)
    assert status == 403
    assert deny["applied"] is False
    status, allow = handle_request("POST", "/update/apply", {"x-api-key": "dev-secret-key", "x-role": "admin"}, req)
    assert status == 200
    assert allow["applied"] is True
