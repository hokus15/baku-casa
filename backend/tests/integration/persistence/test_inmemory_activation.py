from __future__ import annotations

import pytest

from baku.backend.infrastructure.persistence.sqlite.db import get_db_url

pytestmark = pytest.mark.persistence_integration


def test_inmemory_database_is_explicitly_activated(test_db_url: str) -> None:
    active_db_url = get_db_url()

    assert active_db_url == test_db_url
    assert "mode=memory" in active_db_url
