"""Startup configuration validator (EN-0202 / ADR-0013).

Validates a ``ResolvedConfigurationProfile`` against a set of
``ConfigurationParameterDefinition`` instances.

Behaviour:
  - ERRORS: required keys missing from the resolved profile → aggregated into
    ``AggregatedConfigurationError`` and raised (fail-fast).
  - WARNINGS: keys present in the resolved profile that are not declared →
    logged as structured warnings (no startup block).

All errors are collected before raising so that operators can fix the full
set in one cycle.
"""

from __future__ import annotations

import logging
import warnings

from baku.backend.application.configuration.errors import AggregatedConfigurationError
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
        A list of ``ConfigurationValidationIssue`` instances, one per finding.
        Issues with ``severity=ERROR`` will have caused an
        ``AggregatedConfigurationError`` to be raised before the list is
        returned (this list is returned for informational/test purposes even
        in the error path — callers should catch the exception).

    Raises:
        AggregatedConfigurationError: if any required key is absent from the
            resolved profile.
    """
    issues: list[ConfigurationValidationIssue] = []
    declared_keys = {d.key for d in definitions}

    # --- 1. Check required keys ---
    for defn in definitions:
        if defn.required and defn.key not in profile.values:
            issues.append(
                ConfigurationValidationIssue(
                    key=defn.key,
                    severity=ConfigurationIssueSeverity.ERROR,
                    message=f"Required configuration key '{defn.key}' is missing.",
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

    # --- 3. Raise aggregated error if any ERROR-level issues found ---
    error_issues = [i for i in issues if i.severity == ConfigurationIssueSeverity.ERROR]
    if error_issues:
        error_messages = [i.message for i in error_issues]
        raise AggregatedConfigurationError(errors=error_messages)

    return issues
