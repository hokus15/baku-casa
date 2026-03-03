"""Authentication policy configuration — env-config, no DB persistence.

Environment variables are loaded from a .env file (via python-dotenv) so that
local development works without manually exporting variables.  In CI and
production the variables are injected directly into the process environment,
and a .env file is neither required nor consulted (load_dotenv is a no-op when
the variables are already set).

AUTH_JWT_SECRET has **no hard-coded default**.  The application fails fast at
startup when the variable is absent or empty, following ADR-0005 (secrets must
be loaded from configuration/secrets management, never hard-coded).  Tests
supply the secret via monkeypatch.setenv + reset_auth_settings().
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the backend project root (parent of src/).
# load_dotenv is a no-op when the variable already exists in the environment
# (override=False is the default), so CI/production env vars take precedence.
_ENV_FILE = Path(__file__).parent.parent.parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_FILE)


class AuthSettings:
    """Load auth policy from environment variables.

    Raises:
        ValueError: if AUTH_JWT_SECRET is absent or empty.  The application
            must not start with an unknown secret.
    """

    def __init__(self) -> None:
        secret = os.getenv("AUTH_JWT_SECRET", "")
        if not secret:
            raise ValueError(
                "AUTH_JWT_SECRET is not set. "
                "Provide it via the .env file or the process environment. "
                "See backend/.env.example for reference."
            )
        self.jwt_secret: str = secret
        self.jwt_algorithm: str = os.getenv("AUTH_JWT_ALGORITHM", "HS256")
        self.token_ttl_seconds: int = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "3600"))
        self.max_failed_attempts: int = int(os.getenv("AUTH_MAX_FAILED_ATTEMPTS", "5"))
        self.lockout_minutes: int = int(os.getenv("AUTH_LOCKOUT_MINUTES", "15"))


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
