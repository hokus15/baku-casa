from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config

from baku.backend.infrastructure.persistence.sqlite.db import get_db_url


def upgrade_to_head(db_url: str | None = None) -> None:
    backend_root = Path(__file__).resolve().parents[6]
    alembic_ini = backend_root / "alembic.ini"
    migrations_dir = backend_root / "migrations"

    cfg = Config(str(alembic_ini))
    cfg.set_main_option("script_location", str(migrations_dir))
    cfg.set_main_option("sqlalchemy.url", db_url or get_db_url())

    command.upgrade(cfg, "head")
