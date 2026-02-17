from __future__ import annotations
import hashlib
import hmac
import os
from pathlib import Path

from core.models import UpdateApplyRequest

VERSION_FILE = Path("VERSION")
ROLLBACK_DIR = Path("migrations/rollback")


def check_update() -> dict:
    return {"current_version": VERSION_FILE.read_text().strip(), "channel": "stable"}


def verify_signature(payload_sha256: str, signature: str) -> bool:
    key = os.getenv("SERAPHIS_UPDATE_HMAC_KEY", "dev-hmac-key").encode()
    expected = hmac.new(key, payload_sha256.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def apply_update(req: UpdateApplyRequest) -> dict:
    if not verify_signature(req.package.payload_sha256, req.package.signature):
        return {"applied": False, "reason": "signature_verification_failed"}
    prev = VERSION_FILE.read_text().strip()
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLBACK_DIR / f"rollback_from_{req.package.version}.txt").write_text(prev)
    VERSION_FILE.write_text(req.package.version)
    return {"applied": True, "previous": prev, "current": req.package.version}
