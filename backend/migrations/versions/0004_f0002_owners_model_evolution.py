"""Owners model evolution for F-0002.

Renames person_type -> entity_type and updates its values,
removes phone column, adds first_name, last_name, stamp_image,
land_line, land_line_country_code, mobile, mobile_country_code.

Revision ID: 0004_f0002_owners_model_evolution
Revises:     0003_f0002_owners_table
Create Date: 2026-03-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0004_f0002_owners_model_evolution"
down_revision = "0003_f0002_owners_table"
branch_labels = None
depends_on = None

_ENTITY_TYPE_MAP = {
    "FISICA": "PERSONA_FISICA",
    "JURIDICA": "PERSONA_JURIDICA",
}


def upgrade() -> None:
    # 1. Add new identity columns (nullable first, then fill defaults).
    with op.batch_alter_table("owners") as batch_op:
        batch_op.add_column(sa.Column("entity_type", sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column("first_name", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("last_name", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("stamp_image", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("land_line", sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column("land_line_country_code", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("mobile", sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column("mobile_country_code", sa.Integer(), nullable=True))

    # 2. Migrate person_type values to entity_type.
    conn = op.get_bind()
    for old_val, new_val in _ENTITY_TYPE_MAP.items():
        conn.execute(
            sa.text("UPDATE owners SET entity_type = :new WHERE person_type = :old"),
            {"new": new_val, "old": old_val},
        )
    # Any rows with unrecognised values default to PERSONA_FISICA.
    conn.execute(sa.text("UPDATE owners SET entity_type = 'PERSONA_FISICA' WHERE entity_type IS NULL"))

    # 3. Backfill first_name / last_name from legal_name so NOT NULL is satisfied.
    conn.execute(sa.text("UPDATE owners SET first_name = legal_name WHERE first_name IS NULL"))
    conn.execute(sa.text("UPDATE owners SET last_name = '' WHERE last_name IS NULL"))

    # 4. Enforce NOT NULL on newly populated columns and drop old columns.
    with op.batch_alter_table("owners") as batch_op:
        batch_op.alter_column("entity_type", nullable=False)
        batch_op.alter_column("first_name", nullable=False)
        batch_op.alter_column("last_name", nullable=False)
        batch_op.drop_column("person_type")
        batch_op.drop_column("phone")


def downgrade() -> None:
    with op.batch_alter_table("owners") as batch_op:
        batch_op.add_column(sa.Column("person_type", sa.String(length=16), nullable=True))
        batch_op.add_column(sa.Column("phone", sa.String(length=64), nullable=True))

    conn = op.get_bind()
    conn.execute(sa.text("UPDATE owners SET person_type = 'FISICA' WHERE entity_type = 'PERSONA_FISICA'"))
    conn.execute(sa.text("UPDATE owners SET person_type = 'JURIDICA' WHERE entity_type = 'PERSONA_JURIDICA'"))
    conn.execute(sa.text("UPDATE owners SET person_type = 'FISICA' WHERE entity_type = 'ESPJ'"))

    with op.batch_alter_table("owners") as batch_op:
        batch_op.alter_column("person_type", nullable=False)
        batch_op.drop_column("entity_type")
        batch_op.drop_column("first_name")
        batch_op.drop_column("last_name")
        batch_op.drop_column("stamp_image")
        batch_op.drop_column("land_line")
        batch_op.drop_column("land_line_country_code")
        batch_op.drop_column("mobile")
        batch_op.drop_column("mobile_country_code")
