"""Integration test: undeclared keys emit warning without blocking startup (EN-0202 US3).

Verifies that configuration keys present in the resolved profile but not
declared in any ``ConfigurationParameterDefinition`` emit a warning but do
NOT cause a startup failure.
"""

from __future__ import annotations

import warnings

from baku.backend.application.configuration.models import (
    ConfigurationIssueSeverity,
    ConfigurationParameterDefinition,
    ResolvedConfigurationProfile,
)
from baku.backend.infrastructure.config.validator import validate


def test_undeclared_key_does_not_raise():
    """Undeclared key in profile does not raise AggregatedConfigurationError."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
    ]
    profile = ResolvedConfigurationProfile(
        values={"app.secret": "s3cr3t", "unknown.key": "whatever"},
        source_map={"app.secret": "env", "unknown.key": "env"},
    )

    # Must not raise
    issues = validate(profile, definitions)
    warning_issues = [i for i in issues if i.severity == ConfigurationIssueSeverity.WARNING]
    assert len(warning_issues) == 1
    assert warning_issues[0].key == "unknown.key"


def test_undeclared_key_emits_python_warning():
    """Undeclared key triggers a Python ``UserWarning`` via ``warnings.warn``."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
    ]
    profile = ResolvedConfigurationProfile(
        values={"app.secret": "s3cr3t", "stray.key": "oops"},
        source_map={"app.secret": "env", "stray.key": "file"},
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        validate(profile, definitions)

    messages = [str(w.message) for w in caught]
    assert any("stray.key" in m for m in messages)


def test_multiple_undeclared_keys_all_warned():
    """Each undeclared key produces a separate warning issue."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
    ]
    profile = ResolvedConfigurationProfile(
        values={"app.secret": "s3cr3t", "foo.bar": "1", "baz.qux": "2"},
        source_map={"app.secret": "env", "foo.bar": "env", "baz.qux": "env"},
    )

    issues = validate(profile, definitions)
    warning_keys = {i.key for i in issues if i.severity == ConfigurationIssueSeverity.WARNING}
    assert "foo.bar" in warning_keys
    assert "baz.qux" in warning_keys


def test_warn_undeclared_false_suppresses_warnings():
    """Passing ``warn_undeclared=False`` skips the undeclared-key check."""
    definitions = [
        ConfigurationParameterDefinition(key="app.secret", required=True),
    ]
    profile = ResolvedConfigurationProfile(
        values={"app.secret": "s3cr3t", "unknown.key": "whatever"},
        source_map={"app.secret": "env", "unknown.key": "env"},
    )

    issues = validate(profile, definitions, warn_undeclared=False)
    assert all(i.severity != ConfigurationIssueSeverity.WARNING for i in issues)
