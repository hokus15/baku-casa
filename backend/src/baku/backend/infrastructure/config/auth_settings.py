"""Authentication policy configuration — env-config, no DB persistence."""
from __future__ import annotations

import os


class AuthSettings:
    """Load auth policy from environment variables with safe defaults."""

    def __init__(self) -> None:
        self.token_ttl_seconds: int = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "3600"))
        self.max_failed_attempts: int = int(os.getenv("AUTH_MAX_FAILED_ATTEMPTS", "5"))
        self.lockout_minutes: int = int(os.getenv("AUTH_LOCKOUT_MINUTES", "15"))
        self.jwt_secret: str = os.getenv("AUTH_JWT_SECRET", "change-me-in-production")
        self.jwt_algorithm: str = os.getenv("AUTH_JWT_ALGORITHM", "HS256")

        if not self.jwt_secret or self.jwt_secret == "change-me-in-production":
            import warnings

            warnings.warn(
                "AUTH_JWT_SECRET is not set or uses the insecure default. "
                "Set a strong secret in production.",
                stacklevel=2,
            )


_settings: AuthSettings | None = None


def get_auth_settings() -> AuthSettings:
    global _settings
    if _settings is None:
        _settings = AuthSettings()
    return _settings


def reset_auth_settings() -> None:
    """Reset singleton — for use in tests only."""
    global _settings
    _settings = None
