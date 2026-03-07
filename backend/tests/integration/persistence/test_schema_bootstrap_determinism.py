from __future__ import annotations

import pytest
from sqlalchemy import inspect

from baku.backend.infrastructure.persistence.sqlite.db import get_engine

pytestmark = pytest.mark.persistence_integration


def test_migration_bootstrap_produces_expected_schema() -> None:
    engine = get_engine()
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    assert {"operators", "revoked_tokens", "login_throttle_states"}.issubset(tables)
