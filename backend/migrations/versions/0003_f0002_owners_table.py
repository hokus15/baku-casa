"""Create owners table for F-0002.

Revision ID: 0003_f0002_owners_table
Revises:     0002_f0001_operator_singleton_guard
Create Date: 2026-03-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0003_f0002_owners_table"
down_revision = "0002_f0001_operator_singleton_guard"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "owners",
        sa.Column("owner_id", sa.String(length=36), nullable=False),
        sa.Column("person_type", sa.String(length=16), nullable=False),
        sa.Column("legal_name", sa.String(length=512), nullable=False),
        sa.Column("tax_id", sa.String(length=64), nullable=False),
        sa.Column("fiscal_address_line1", sa.String(length=512), nullable=False),
        sa.Column("fiscal_address_city", sa.String(length=255), nullable=False),
        sa.Column("fiscal_address_postal_code", sa.String(length=20), nullable=False),
        sa.Column("fiscal_address_country", sa.String(length=2), nullable=False, server_default="ES"),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.Column("deleted_at", sa.String(length=32), nullable=True),
        sa.Column("deleted_by", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("owner_id"),
    )
    op.create_index("ix_owners_tax_id", "owners", ["tax_id"])
    op.create_index("ix_owners_deleted_at", "owners", ["deleted_at"])


def downgrade() -> None:
    op.drop_index("ix_owners_deleted_at", table_name="owners")
    op.drop_index("ix_owners_tax_id", table_name="owners")
    op.drop_table("owners")
