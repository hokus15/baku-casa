"""Configuration source loaders for the centralized configuration system (EN-0202).

Each loader returns a flat ``dict[str, str]`` mapping of canonical keys to raw
string values loaded from a specific source.  The resolver (``resolver.py``)
applies precedence rules over these outputs.

Sources (in precedence order, highest first):
  env  — process environment variables (os.environ)
  file — .env file loaded via python-dotenv (does not override env by default)
  default — built-in application defaults

Design constraints (ADR-0013):
  - ``os.getenv`` / ``os.environ`` access is ONLY permitted inside this module.
  - All other modules must obtain values through the ConfigurationProviderPort.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import dotenv_values

# ---------------------------------------------------------------------------
# Source loaders
# ---------------------------------------------------------------------------

# Mapping from env-var name to canonical dot-notation key.
# Extend this mapping whenever a new configuration key is introduced.
_ENV_VAR_TO_KEY: dict[str, str] = {
    "DATABASE_URL": "persistence.database_url",
    "AUTH_JWT_SECRET": "auth.jwt_secret",
    "AUTH_JWT_ALGORITHM": "auth.jwt_algorithm",
    "AUTH_TOKEN_TTL_SECONDS": "auth.token_ttl_seconds",
    "AUTH_MAX_FAILED_ATTEMPTS": "auth.max_failed_attempts",
    "AUTH_LOCKOUT_MINUTES": "auth.lockout_minutes",
}

_TEST_DB_ENV_VAR = "TEST_DATABASE_URL"

# Reverse mapping: canonical key → env-var name (for diagnostic messages).
_KEY_TO_ENV_VAR: dict[str, str] = {v: k for k, v in _ENV_VAR_TO_KEY.items()}

# Built-in defaults for optional keys.
_DEFAULTS: dict[str, str] = {
    "persistence.database_url": "sqlite:///./baku.db",
    "auth.jwt_algorithm": "HS256",
    "auth.token_ttl_seconds": "3600",
    "auth.max_failed_attempts": "5",
    "auth.lockout_minutes": "15",
}


def load_env_source() -> dict[str, str]:
    """Return configuration values from the process environment.

    Only keys declared in ``_ENV_VAR_TO_KEY`` are mapped; undeclared env vars
    are ignored at this level (warning logic lives in the validator).
    """
    result: dict[str, str] = {}
    test_db_url = os.environ.get(_TEST_DB_ENV_VAR)
    if test_db_url is not None:
        result["persistence.database_url"] = test_db_url

    for env_var, key in _ENV_VAR_TO_KEY.items():
        if key == "persistence.database_url" and "persistence.database_url" in result:
            continue
        value = os.environ.get(env_var)
        if value is not None:
            result[key] = value
    return result


def load_file_source(env_file: Path | None = None) -> dict[str, str]:
    """Return configuration values from a .env file.

    Values already present in the environment are NOT overridden (consistent
    with the ``load_dotenv(override=False)`` semantics used elsewhere).

    Args:
        env_file: Path to the .env file.  When ``None`` the default location
            ``<backend-root>/.env`` is used.  Pass an explicit empty path
            (``Path("")``) or a non-existent path to skip file loading.
    """
    if env_file is None:
        # Derive from module location: src/baku/backend/infrastructure/config/
        # → six levels up → backend root
        env_file = Path(__file__).parent.parent.parent.parent.parent.parent / ".env"

    if not env_file.exists():
        return {}

    raw: dict[str, str | None] = dotenv_values(dotenv_path=env_file)
    result: dict[str, str] = {}

    if _TEST_DB_ENV_VAR not in os.environ:
        test_db_url = raw.get(_TEST_DB_ENV_VAR)
        if test_db_url is not None:
            result["persistence.database_url"] = test_db_url

    for env_var, key in _ENV_VAR_TO_KEY.items():
        if key == "persistence.database_url" and "persistence.database_url" in result:
            continue
        # Skip if already present in the process environment (env has higher precedence)
        if env_var in os.environ:
            continue
        value = raw.get(env_var)
        if value is not None:
            result[key] = value
    return result


def load_default_source() -> dict[str, str]:
    """Return built-in application default values."""
    return dict(_DEFAULTS)


def all_declared_keys() -> frozenset[str]:
    """Return the set of all canonical keys known to the configuration system."""
    return frozenset(_ENV_VAR_TO_KEY.values())


def env_var_for_key(key: str) -> str | None:
    """Return the environment variable name for a canonical key, or ``None``."""
    return _KEY_TO_ENV_VAR.get(key)
