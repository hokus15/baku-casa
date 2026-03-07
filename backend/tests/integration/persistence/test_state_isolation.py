from __future__ import annotations

import pytest
from sqlalchemy import text

from baku.backend.infrastructure.persistence.sqlite.db import get_session_factory

pytestmark = pytest.mark.persistence_integration


def test_schema_starts_clean_for_each_test() -> None:
    factory = get_session_factory()
    with factory() as session:
        count = session.execute(text("SELECT COUNT(*) FROM operators")).scalar_one()

    assert count == 0
