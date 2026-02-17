import os

API_KEY_ENV = "SERAPHIS_API_KEY"


def is_valid_api_key(candidate: str) -> bool:
    configured = os.getenv(API_KEY_ENV, "dev-secret-key")
    return candidate == configured
