"""Typed configuration validation error types (EN-0202).

Application layer only — no infrastructure imports.
"""

from __future__ import annotations

from dataclasses import dataclass


class ConfigurationError(Exception):
    """Base class for all configuration-related startup errors."""


@dataclass
class MissingRequiredKeyError(ConfigurationError):
    """Raised when one or more required configuration keys are absent.

    Attributes:
        missing_keys: Sequence of required keys that were not resolved.
    """

    missing_keys: list[str]

    def __str__(self) -> str:
        keys = ", ".join(self.missing_keys)
        return (
            f"Startup aborted: required configuration key(s) missing: {keys}. "
            "Provide the key(s) via environment variables, a .env file, or the "
            "application configuration file."
        )


@dataclass
class AggregatedConfigurationError(ConfigurationError):
    """Raised when multiple configuration validation errors are detected.

    All errors are collected before aborting so that operators can fix
    the complete set in one cycle (ADR-0013 fail-fast semantics).

    Attributes:
        errors: Human-readable error messages, one per failing key.
    """

    errors: list[str]

    def __str__(self) -> str:
        lines = "\n  - ".join(self.errors)
        return f"Startup aborted: {len(self.errors)} configuration error(s):\n  - {lines}"
