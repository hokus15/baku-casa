from __future__ import annotations

from collections.abc import Generator

import pytest

from baku.backend.infrastructure.config.runtime_settings import RuntimeConfigurationProvider, reset_runtime_settings


@pytest.fixture(autouse=True)
def _reset_provider() -> Generator[None, None, None]:
    reset_runtime_settings()
    yield
    reset_runtime_settings()


def test_test_database_profile_is_explicitly_activated(monkeypatch) -> None:
    monkeypatch.setenv("AUTH_JWT_SECRET", "activation-secret")
    monkeypatch.setenv("TEST_DATABASE_URL", "sqlite+pysqlite:///file:activation?mode=memory&cache=shared&uri=true")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./runtime.db")

    profile = RuntimeConfigurationProvider(env_file=None).get_profile()

    assert profile.require("persistence.database_url").startswith("sqlite+pysqlite:///file:activation")
    assert profile.source_map.get("persistence.database_url") == "env"
