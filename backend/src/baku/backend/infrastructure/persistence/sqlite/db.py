"""SQLite engine and session factory.

Schema lifecycle is managed through versioned migrations (ADR-0003),
not via runtime metadata creation.

The database URL is resolved through the centralized configuration provider
(ADR-0013); no direct ``os.getenv`` calls are made here.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from baku.backend.infrastructure.config.runtime_settings import RuntimeConfigurationProvider

_engine: Engine | None = None
_SessionFactory: sessionmaker[Session] | None = None


def get_db_url() -> str:
    return RuntimeConfigurationProvider().get_profile().require("persistence.database_url")


def _is_sqlite_memory_url(url: str) -> bool:
    """Return True when URL points to an in-memory SQLite database."""
    if not url.startswith("sqlite"):
        return False
    return url == "sqlite://" or "mode=memory" in url


def get_engine(url: str | None = None) -> Engine:
    global _engine
    if _engine is None:
        resolved_url = url or get_db_url()
        # SQLite in-memory databases require StaticPool so all connections
        # in this process reuse the same transient DB lifecycle.
        is_memory = _is_sqlite_memory_url(resolved_url)
        connect_args: dict[str, Any] = {"check_same_thread": False}
        if "uri=true" in resolved_url:
            connect_args["uri"] = True
        kwargs: dict[str, Any] = {"connect_args": connect_args}
        if is_memory:
            kwargs["poolclass"] = StaticPool
        _engine = create_engine(resolved_url, **kwargs)
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
