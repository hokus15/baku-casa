"""Add partial unique index on owners.tax_id for active records.

Ensures tax_id uniqueness among non-deleted owners at the DB level,
preventing race-condition duplicates that application-layer checks alone
cannot prevent.

Revision ID: 0005_f0002_owners_tax_id_unique_index
Revises:     0004_f0002_owners_model_evolution
Create Date: 2026-03-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0005_f0002_owners_tax_id_unique_index"
down_revision = "0004_f0002_owners_model_evolution"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "CREATE UNIQUE INDEX IF NOT EXISTS uix_owners_tax_id_active "
            "ON owners (tax_id) WHERE deleted_at IS NULL"
        )
    )


def downgrade() -> None:
    op.drop_index("uix_owners_tax_id_active", table_name="owners")
