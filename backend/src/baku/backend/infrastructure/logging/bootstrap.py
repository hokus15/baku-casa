"""Framework logging bootstrap for EN-0200."""

from __future__ import annotations

import logging
import logging.config
import os
from pathlib import Path

from baku.backend.infrastructure.logging.context import (
    CorrelationIdFilter,
    ServiceNameFilter,
)
from baku.backend.infrastructure.logging.formatters import JsonLogFormatter

_ENV_TO_PROFILE = {
    "dev": "logging.dev.ini",
    "test": "logging.test.ini",
    "prod": "logging.prod.ini",
}


def resolve_logging_environment() -> str:
    """Resolve active runtime environment for logging profile selection."""
    value = (
        (os.getenv("APP_ENV") or os.getenv("ENVIRONMENT") or "dev")
        .strip()
        .lower()
    )
    return value if value in _ENV_TO_PROFILE else "dev"


def resolve_logging_profile_filename(environment: str) -> str:
    """Map environment to root profile filename."""
    return _ENV_TO_PROFILE.get(environment, "logging.dev.ini")


def _repo_backend_root() -> Path:
    """Locate the backend project root, working both from source and installed packages."""
    cwd = Path.cwd()
    for candidate in [cwd, *cwd.parents]:
        if any(
            (candidate / name).exists() for name in _ENV_TO_PROFILE.values()
        ):
            return candidate
    # Fallback: __file__-relative (works for editable installs running from source)
    # backend/src/baku/backend/infrastructure/logging/bootstrap.py -> backend/
    return Path(__file__).resolve().parents[5]


def _install_record_filters(environment: str) -> None:
    root = logging.getLogger()
    root.filters.clear()
    root.addFilter(CorrelationIdFilter())
    root.addFilter(
        ServiceNameFilter(service_name="baku-backend", environment=environment)
    )
    for handler in root.handlers:
        handler.filters.clear()
        handler.addFilter(CorrelationIdFilter())
        handler.addFilter(
            ServiceNameFilter(
                service_name="baku-backend", environment=environment
            )
        )


def _console_fallback_formatter(environment: str) -> logging.Formatter:
    if environment == "prod":
        return JsonLogFormatter()
    if environment == "test":
        # Deterministic compact output for test assertions.
        return logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(service_name)s correlation_id=%(correlation_id)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    return logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(service_name)s correlation_id=%(correlation_id)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


def _apply_safe_fallback(environment: str, reason: str) -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(_console_fallback_formatter(environment))
    root.addHandler(handler)

    _install_record_filters(environment)

    logging.getLogger(__name__).warning(
        "logging_profile_fallback_applied",
        extra={"environment": environment, "reason": reason},
    )


def configure_framework_logging() -> None:
    """Load logging profile from backend root, with safe console fallback."""
    environment = resolve_logging_environment()
    profile_name = resolve_logging_profile_filename(environment)
    root_dir = _repo_backend_root()
    (root_dir / "logs").mkdir(parents=True, exist_ok=True)
    profile_path = root_dir / profile_name

    if profile_path.exists():
        try:
            logging.config.fileConfig(
                profile_path, disable_existing_loggers=False
            )
            _install_record_filters(environment)
            return
        except (
            Exception
        ) as exc:  # pragma: no cover - tested via integration fallback tests
            _apply_safe_fallback(
                environment, f"invalid_profile:{type(exc).__name__}"
            )
            return

    _apply_safe_fallback(environment, "missing_profile")
