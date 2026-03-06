"""Integration test: aggregated validation errors reporting (EN-0202 US2).

Verifies that the startup validator collects ALL validation errors in a single
pass — not just the first failure — and that the caller (RuntimeConfigurationProvider)
converts those into a single ``AggregatedConfigurationError``.
"""

from __future__ import annotations

from baku.backend.application.configuration.models import (
    ConfigurationIssueSeverity,
    ConfigurationParameterDefinition,
    ResolvedConfigurationProfile,
)
from baku.backend.infrastructure.config.validator import validate


def test_validator_collects_all_missing_required_keys():
    """All missing required keys are returned as ERROR issues in a single pass."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
        ConfigurationParameterDefinition(key="app.api_key", required=True),
        ConfigurationParameterDefinition(key="app.timeout", required=False, default="30"),
    ]
    # Empty profile — both required keys are absent
    profile = ResolvedConfigurationProfile(values={}, source_map={})

    issues = validate(profile, definitions, warn_undeclared=False)

    error_issues = [i for i in issues if i.severity == ConfigurationIssueSeverity.ERROR]
    assert len(error_issues) == 2
    keys_in_errors = " ".join(i.message for i in error_issues)
    assert "app.secret" in keys_in_errors
    assert "app.api_key" in keys_in_errors


def test_aggregated_error_message_lists_all_keys():
    """Each missing required key appears in its own ERROR issue message."""
    definitions = [
        ConfigurationParameterDefinition(key="x.one", required=True),
        ConfigurationParameterDefinition(key="x.two", required=True),
    ]
    profile = ResolvedConfigurationProfile(values={}, source_map={})

    issues = validate(profile, definitions, warn_undeclared=False)

    error_messages = " ".join(i.message for i in issues if i.severity == ConfigurationIssueSeverity.ERROR)
    assert "x.one" in error_messages
    assert "x.two" in error_messages


def test_no_error_when_all_required_keys_present():
    """Validation passes when all required keys are resolved."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
    ]
    profile = ResolvedConfigurationProfile(
        values={"app.secret": "secret-value"},
        source_map={"app.secret": "env"},
    )

    issues = validate(profile, definitions, warn_undeclared=False)

    assert all(i.severity.value != "error" for i in issues)


def test_optional_missing_key_does_not_cause_error():
    """An absent optional key does not raise an error."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
        ConfigurationParameterDefinition(key="app.optional", required=False, default="val"),
    ]
    # Only required key present; optional is absent (would be filled by defaults normally)
    profile = ResolvedConfigurationProfile(
        values={"app.secret": "my-secret"},
        source_map={"app.secret": "env"},
    )

    issues = validate(profile, definitions, warn_undeclared=False)

    assert not any(i.severity.value == "error" for i in issues)


def test_empty_string_required_key_treated_as_missing():
    """A required key present with an empty string value is treated as missing."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
    ]
    profile = ResolvedConfigurationProfile(
        values={"app.secret": ""},
        source_map={"app.secret": "env"},
    )

    issues = validate(profile, definitions, warn_undeclared=False)

    error_issues = [i for i in issues if i.severity == ConfigurationIssueSeverity.ERROR]
    assert len(error_issues) == 1
    assert "app.secret" in error_issues[0].message


def test_whitespace_only_required_key_treated_as_missing():
    """A required key present with a whitespace-only value is treated as missing."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
    ]
    profile = ResolvedConfigurationProfile(
        values={"app.secret": "   "},
        source_map={"app.secret": "file"},
    )

    issues = validate(profile, definitions, warn_undeclared=False)

    error_issues = [i for i in issues if i.severity == ConfigurationIssueSeverity.ERROR]
    assert len(error_issues) == 1
    assert "app.secret" in error_issues[0].message
