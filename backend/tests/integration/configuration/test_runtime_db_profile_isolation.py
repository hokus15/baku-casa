from __future__ import annotations

from collections.abc import Generator

import pytest

from baku.backend.infrastructure.config.runtime_settings import RuntimeConfigurationProvider, reset_runtime_settings


@pytest.fixture(autouse=True)
def _reset_provider() -> Generator[None, None, None]:
    reset_runtime_settings()
    yield
    reset_runtime_settings()


def test_runtime_profile_uses_standard_database_url_when_test_override_missing(monkeypatch) -> None:
    monkeypatch.setenv("AUTH_JWT_SECRET", "runtime-secret")
    monkeypatch.delenv("TEST_DATABASE_URL", raising=False)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./runtime.db")

    profile = RuntimeConfigurationProvider(env_file=None).get_profile()

    assert profile.require("persistence.database_url") == "sqlite:///./runtime.db"
