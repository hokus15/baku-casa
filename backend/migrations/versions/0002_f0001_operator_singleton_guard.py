"""Add singleton_guard to operators table.

Enforces the single-operator invariant at the database level (ADR-0005, FR-001).
The UNIQUE + CHECK constraints on singleton_guard = 1 mean only one row can
ever be inserted, making concurrent bootstrap calls atomic: one succeeds and
the other receives an IntegrityError that the repository maps to
BootstrapAlreadyCompleted (→ HTTP 409).

Revision ID: 0002_f0001_operator_singleton_guard
Revises:     0001_f0001_auth_tables
Create Date: 2026-03-03
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_f0001_operator_singleton_guard"
down_revision = "0001_f0001_auth_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite does not support ALTER TABLE ADD CONSTRAINT, so batch mode is used
    # to rebuild the table with the new column and constraints in one operation.
    with op.batch_alter_table("operators", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "singleton_guard",
                sa.Integer(),
                nullable=False,
                server_default="1",
            )
        )
        batch_op.create_unique_constraint("uq_operators_singleton", ["singleton_guard"])
        batch_op.create_check_constraint("ck_operators_singleton_is_1", "singleton_guard = 1")


def downgrade() -> None:
    with op.batch_alter_table("operators", schema=None) as batch_op:
        batch_op.drop_constraint("ck_operators_singleton_is_1", type_="check")
        batch_op.drop_constraint("uq_operators_singleton", type_="unique")
        batch_op.drop_column("singleton_guard")
