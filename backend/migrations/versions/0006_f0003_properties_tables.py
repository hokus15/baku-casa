"""Create properties and ownerships tables for F-0003.

Revision ID: 0006_f0003_properties_tables
Revises:     0005_f0002_owners_tax_id_unique_index
Create Date: 2026-03-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0006_f0003_properties_tables"
down_revision = "0005_f0002_owners_tax_id_unique_index"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "properties",
        sa.Column("property_id", sa.String, primary_key=True, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("address", sa.String, nullable=True),
        sa.Column("city", sa.String, nullable=True),
        sa.Column("postal_code", sa.String, nullable=True),
        sa.Column("province", sa.String, nullable=True),
        sa.Column("country", sa.String, nullable=True),
        sa.Column("cadastral_reference", sa.String, nullable=True),
        sa.Column("cadastral_value", sa.String, nullable=True),
        sa.Column("cadastral_land_value", sa.String, nullable=True),
        sa.Column("cadastral_value_revised", sa.String, nullable=True),
        sa.Column("acquisition_date", sa.String, nullable=True),
        sa.Column("acquisition_type", sa.String, nullable=True),
        sa.Column("transfer_date", sa.String, nullable=True),
        sa.Column("transfer_type", sa.String, nullable=True),
        sa.Column("fiscal_nature", sa.String, nullable=True),
        sa.Column("fiscal_situation", sa.String, nullable=True),
        sa.Column("created_at", sa.String, nullable=False),
        sa.Column("updated_at", sa.String, nullable=False),
        sa.Column("deleted_at", sa.String, nullable=True),
        sa.Column("created_by", sa.String, nullable=False),
        sa.Column("updated_by", sa.String, nullable=False),
        sa.Column("deleted_by", sa.String, nullable=True),
    )
    op.create_index("ix_properties_deleted_at", "properties", ["deleted_at"])

    op.create_table(
        "ownerships",
        sa.Column("ownership_id", sa.String, primary_key=True, nullable=False),
        sa.Column(
            "property_id",
            sa.String,
            sa.ForeignKey("properties.property_id"),
            nullable=False,
        ),
        sa.Column(
            "owner_id",
            sa.String,
            sa.ForeignKey("owners.owner_id"),
            nullable=False,
        ),
        sa.Column("ownership_percentage", sa.String, nullable=False),
        sa.Column("created_at", sa.String, nullable=False),
        sa.Column("updated_at", sa.String, nullable=False),
        sa.Column("deleted_at", sa.String, nullable=True),
        sa.Column("created_by", sa.String, nullable=False),
        sa.Column("updated_by", sa.String, nullable=False),
        sa.Column("deleted_by", sa.String, nullable=True),
    )
    op.create_index("ix_ownerships_property_id", "ownerships", ["property_id"])
    op.create_index("ix_ownerships_owner_id", "ownerships", ["owner_id"])
    op.create_index("ix_ownerships_deleted_at", "ownerships", ["deleted_at"])


def downgrade() -> None:
    op.drop_table("ownerships")
    op.drop_table("properties")
