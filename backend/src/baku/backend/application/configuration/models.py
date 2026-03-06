"""Typed configuration models for the centralized configuration system (EN-0202).

These models belong to the Application layer.  No framework or infrastructure
imports are allowed here (ADR-0002).
"""

from __future__ import annotations

import types
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class ConfigurationIssueSeverity(str, Enum):
    """Severity level of a configuration validation issue."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class ConfigurationParameterDefinition:
    """Describes a known configuration parameter and its policy.

    Attributes:
        key: Canonical dot-notation key (e.g. ``"auth.jwt_secret"``).
        required: Whether the parameter must be present at startup.
        default: Default value used when the parameter is absent from all
            sources.  Must be ``None`` when *required* is ``True``.
        description: Human-readable description for diagnostic output.
    """

    key: str
    required: bool
    default: str | None = None
    description: str = ""

    def __post_init__(self) -> None:
        if self.required and self.default is not None:
            raise ValueError(f"Parameter '{self.key}' is required; it must not have a default.")


@dataclass(frozen=True)
class ResolvedConfigurationProfile:
    """Immutable snapshot of fully-resolved configuration values.

    Both *values* and *source_map* are wrapped in ``types.MappingProxyType``
    on construction, so the stored mappings are truly read-only.  Callers may
    pass plain ``dict`` objects; a copy is taken before wrapping.

    Attributes:
        values: Read-only mapping of canonical key → resolved string value.
        source_map: Read-only mapping of canonical key → source name
            (``"env"``, ``"file"``, or ``"default"``).
    """

    values: Mapping[str, str]
    source_map: Mapping[str, str]

    def __post_init__(self) -> None:
        # Take a shallow copy then wrap in MappingProxyType so that neither
        # the original dict nor the proxy can mutate the stored data.
        object.__setattr__(self, "values", types.MappingProxyType(dict(self.values)))
        object.__setattr__(self, "source_map", types.MappingProxyType(dict(self.source_map)))

    def get(self, key: str) -> str | None:
        """Return the resolved value for *key*, or ``None`` if absent."""
        return self.values.get(key)

    def require(self, key: str) -> str:
        """Return the resolved value for *key*.

        Raises:
            KeyError: if *key* is not present in the resolved profile.
        """
        try:
            return self.values[key]
        except KeyError:
            raise KeyError(f"Configuration key '{key}' not found in resolved profile.") from None


@dataclass(frozen=True)
class ConfigurationValidationIssue:
    """A single validation finding produced during startup validation.

    Attributes:
        key: The configuration key this issue relates to.
        severity: ``ERROR`` aborts startup; ``WARNING`` is logged but allowed.
        message: Human-readable description of the issue.
    """

    key: str
    severity: ConfigurationIssueSeverity
    message: str
