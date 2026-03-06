"""Startup configuration validator (EN-0202 / ADR-0013).

Validates a ``ResolvedConfigurationProfile`` against a set of
``ConfigurationParameterDefinition`` instances.

Behaviour:
  - ERRORS: required keys missing or blank in the resolved profile → returned
    as ``ConfigurationValidationIssue`` items with ``severity=ERROR``.
    The caller is responsible for inspecting the list and raising if needed.
  - WARNINGS: keys present in the resolved profile that are not declared →
    returned as WARNING-severity issues and logged (no startup block).

All issues are collected in one pass so that operators can fix the full set
in a single cycle.
"""

from __future__ import annotations

import logging
import warnings

from baku.backend.application.configuration.models import (
    ConfigurationIssueSeverity,
    ConfigurationParameterDefinition,
    ConfigurationValidationIssue,
    ResolvedConfigurationProfile,
)

logger = logging.getLogger(__name__)


def validate(
    profile: ResolvedConfigurationProfile,
    definitions: list[ConfigurationParameterDefinition],
    *,
    warn_undeclared: bool = True,
) -> list[ConfigurationValidationIssue]:
    """Validate *profile* against *definitions*.

    Args:
        profile: The fully-resolved configuration profile to validate.
        definitions: The set of declared configuration parameter definitions.
        warn_undeclared: When ``True`` (default), emit a WARNING for every key
            present in the profile that is not covered by any definition.

    Returns:
        A list of all ``ConfigurationValidationIssue`` instances found,
        including both ERROR and WARNING severities.  The function never
        raises; the caller is responsible for checking for ERROR-level issues
        and raising ``AggregatedConfigurationError`` (or any other action) as
        appropriate.
    """
    issues: list[ConfigurationValidationIssue] = []
    declared_keys = {d.key for d in definitions}

    # --- 1. Check required keys (absent OR blank/whitespace-only) ---
    for defn in definitions:
        if defn.required and not profile.values.get(defn.key, "").strip():
            issues.append(
                ConfigurationValidationIssue(
                    key=defn.key,
                    severity=ConfigurationIssueSeverity.ERROR,
                    message=f"Required configuration key '{defn.key}' is missing or blank.",
                )
            )

    # --- 2. Check for undeclared keys ---
    if warn_undeclared:
        for key in profile.values:
            if key not in declared_keys:
                issue = ConfigurationValidationIssue(
                    key=key,
                    severity=ConfigurationIssueSeverity.WARNING,
                    message=(
                        f"Undeclared configuration key '{key}' found in resolved "
                        "profile. This key is not part of the known configuration "
                        "schema. Remove it or declare it explicitly."
                    ),
                )
                issues.append(issue)
                # Emit as a Python warning AND a structured log entry so that
                # both test-capture mechanisms and log aggregators see it.
                warnings.warn(issue.message, stacklevel=2)
                logger.warning(
                    "undeclared_config_key",
                    extra={"key": key, "severity": "WARNING"},
                )

    return issues
