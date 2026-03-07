from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config

from baku.backend.infrastructure.persistence.sqlite.db import (
    is_sqlite_memory_url,
    get_db_url,
    get_engine,
)


def upgrade_to_head(db_url: str | None = None) -> None:
    backend_root = Path(__file__).resolve().parents[6]
    alembic_ini = backend_root / "alembic.ini"
    migrations_dir = backend_root / "migrations"

    resolved_db_url = db_url or get_db_url()

    cfg = Config(str(alembic_ini))
    cfg.set_main_option("script_location", str(migrations_dir))
    cfg.set_main_option("sqlalchemy.url", resolved_db_url)

    if is_sqlite_memory_url(resolved_db_url):
        # Initialise (or reuse) the application engine for resolved_db_url so
        # the migrated schema is visible to all sessions in the in-memory lifecycle.
        with get_engine(resolved_db_url).connect() as connection:
            cfg.attributes["connection"] = connection
            command.upgrade(cfg, "head")
        return

    command.upgrade(cfg, "head")
