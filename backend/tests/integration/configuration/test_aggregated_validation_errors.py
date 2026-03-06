"""Integration test: aggregated validation errors reporting (EN-0202 US2).

Verifies that the startup validator collects ALL validation errors in a single
pass and raises a single ``AggregatedConfigurationError`` containing the full
error set — not just the first failure.
"""

from __future__ import annotations

import pytest

from baku.backend.application.configuration.errors import AggregatedConfigurationError
from baku.backend.application.configuration.models import (
    ConfigurationParameterDefinition,
    ResolvedConfigurationProfile,
)
from baku.backend.infrastructure.config.validator import validate


def test_validator_collects_all_missing_required_keys():
    """All missing required keys appear in the aggregated error at once."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
        ConfigurationParameterDefinition(key="app.api_key", required=True),
        ConfigurationParameterDefinition(key="app.timeout", required=False, default="30"),
    ]
    # Empty profile — both required keys are absent
    profile = ResolvedConfigurationProfile(values={}, source_map={})

    with pytest.raises(AggregatedConfigurationError) as exc_info:
        validate(profile, definitions)

    error = exc_info.value
    assert len(error.errors) == 2
    keys_in_errors = " ".join(error.errors)
    assert "app.secret" in keys_in_errors
    assert "app.api_key" in keys_in_errors


def test_aggregated_error_message_lists_all_keys():
    """The string representation of the error names every missing key."""
    definitions = [
        ConfigurationParameterDefinition(key="x.one", required=True),
        ConfigurationParameterDefinition(key="x.two", required=True),
    ]
    profile = ResolvedConfigurationProfile(values={}, source_map={})

    with pytest.raises(AggregatedConfigurationError) as exc_info:
        validate(profile, definitions)

    msg = str(exc_info.value)
    assert "x.one" in msg
    assert "x.two" in msg


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
