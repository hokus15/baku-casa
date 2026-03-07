from __future__ import annotations

import pytest
from sqlalchemy import inspect

from baku.backend.infrastructure.persistence.sqlite.db import get_engine

pytestmark = pytest.mark.persistence_integration


def test_repeated_schema_inspection_is_consistent() -> None:
    engine = get_engine()
    inspector = inspect(engine)

    first = sorted(inspector.get_table_names())
    second = sorted(inspector.get_table_names())

    assert first == second
