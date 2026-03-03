"""SQLite engine and session factory.

Schema lifecycle is managed through versioned migrations (ADR-0003),
not via runtime metadata creation.
"""

from __future__ import annotations

import os
from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

_engine: Engine | None = None
_SessionFactory: sessionmaker[Session] | None = None


def get_db_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./baku.db")


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        url = get_db_url()
        # SQLite in-memory databases (sqlite://) require StaticPool so all
        # connections within the same process share the same in-memory DB.
        is_memory = url == "sqlite://"
        kwargs: dict[str, Any] = {"connect_args": {"check_same_thread": False}}
        if is_memory:
            kwargs["poolclass"] = StaticPool
        _engine = create_engine(url, **kwargs)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return _SessionFactory


def reset_engine() -> None:
    """Reset engine singleton — for use in tests only."""
    global _engine, _SessionFactory
    _engine = None
    _SessionFactory = None
