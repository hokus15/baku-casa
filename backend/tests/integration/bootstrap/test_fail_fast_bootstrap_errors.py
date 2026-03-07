"""Integration test: fail-fast bootstrap critical errors (US3).

Verifies that the bootstrap lifespan enforces fail-fast semantics on missing
critical configuration, consistent with ADR-0013.

Note on test isolation: The backend root contains a `.env` file used for local
development. Tests that need to isolate the config source from file loading must
pass an explicit non-existent `env_file` path to RuntimeConfigurationProvider
(the same pattern used in tests/integration/configuration/).

Spec: FR-011 — explicit fail-fast behavior on missing critical startup configuration.
ADR-0013 — centralized configuration with fail-fast on missing required keys.
"""

from __future__ import annotations

import inspect

import pytest
from fastapi.testclient import TestClient

from baku.backend.application.configuration.errors import AggregatedConfigurationError
from baku.backend.infrastructure.config.runtime_settings import (
    RuntimeConfigurationProvider,
    reset_runtime_settings,
)


def test_lifespan_invokes_get_profile_for_fail_fast() -> None:
    """lifespan.py must invoke RuntimeConfigurationProvider().get_profile() — the fail-fast entry point (ADR-0013)."""
    import baku.backend.interfaces.http.bootstrap.lifespan as lifespan_mod

    source = inspect.getsource(lifespan_mod)
    assert (
        "RuntimeConfigurationProvider" in source
    ), "lifespan.py must use RuntimeConfigurationProvider for centralized config validation"
    assert (
        "get_profile()" in source
    ), "lifespan.py must call get_profile() which enforces fail-fast on missing required keys (ADR-0013)"


def test_fail_fast_raises_aggregated_error_on_missing_jwt_secret(monkeypatch, tmp_path) -> None:
    """Startup config validation must raise AggregatedConfigurationError when AUTH_JWT_SECRET is absent.

    Uses a non-existent env_file (as in the configuration integration tests) to prevent
    the local .env file from supplying the missing secret.
    """
    monkeypatch.delenv("AUTH_JWT_SECRET", raising=False)
    reset_runtime_settings()

    provider = RuntimeConfigurationProvider(env_file=tmp_path / ".env")

    with pytest.raises(AggregatedConfigurationError) as exc_info:
        provider.get_profile()

    assert "auth.jwt_secret" in str(
        exc_info.value
    ), "AggregatedConfigurationError must mention the missing key 'auth.jwt_secret'"


def test_lifespan_handler_succeeds_when_config_is_valid(monkeypatch) -> None:
    """Lifespan handler must complete normally when all required env vars are present.

    All required env vars are supplied by the autouse _reset_singletons fixture.
    """
    from baku.backend.main import app

    with TestClient(app, raise_server_exceptions=True) as client:
        resp = client.get("/openapi.json")
    assert resp.status_code == 200


def test_lifespan_calls_init_auth_settings() -> None:
    """lifespan.py must call init_auth_settings — deriving auth config from the validated profile."""
    import baku.backend.interfaces.http.bootstrap.lifespan as lifespan_mod

    source = inspect.getsource(lifespan_mod)
    assert (
        "init_auth_settings" in source
    ), "lifespan.py must call init_auth_settings() to derive auth config from the validated profile"
