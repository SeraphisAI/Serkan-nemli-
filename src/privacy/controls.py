SENSITIVE_FIELDS = {"location"}


def classify(field: str) -> str:
    return "sensitive" if field in SENSITIVE_FIELDS else "public"


def mask_payload(payload: dict) -> dict:
    masked = {}
    for key, value in payload.items():
        masked[key] = "***" if key in SENSITIVE_FIELDS else value
    return masked
