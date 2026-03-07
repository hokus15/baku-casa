from __future__ import annotations

from collections.abc import Generator

import pytest

from baku.backend.infrastructure.config.runtime_settings import RuntimeConfigurationProvider, reset_runtime_settings


@pytest.fixture(autouse=True)
def _reset_provider() -> Generator[None, None, None]:
    reset_runtime_settings()
    yield
    reset_runtime_settings()


def test_test_database_url_has_precedence_over_database_url(monkeypatch) -> None:
    monkeypatch.setenv("AUTH_JWT_SECRET", "precedence-secret")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./runtime.db")
    monkeypatch.setenv("TEST_DATABASE_URL", "sqlite+pysqlite:///file:precedence?mode=memory&cache=shared&uri=true")

    profile = RuntimeConfigurationProvider(env_file=None).get_profile()

    assert profile.require("persistence.database_url") == (
        "sqlite+pysqlite:///file:precedence?mode=memory&cache=shared&uri=true"
    )
