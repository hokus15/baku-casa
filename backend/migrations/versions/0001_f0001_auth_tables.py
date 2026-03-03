"""Create authentication tables for F-0001.

Revision ID: 0001_f0001_auth_tables
Revises:
Create Date: 2026-03-03
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_f0001_auth_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "operators",
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("credential_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=True),
        sa.Column("last_login_at", sa.String(length=32), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("operator_id"),
        sa.UniqueConstraint("username"),
    )

    op.create_table(
        "revoked_tokens",
        sa.Column("token_jti", sa.String(length=255), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("revoked_at", sa.String(length=32), nullable=False),
        sa.Column("expires_at", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.operator_id"]),
        sa.PrimaryKeyConstraint("token_jti"),
    )

    op.create_table(
        "login_throttle_states",
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("failed_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("blocked_until", sa.String(length=32), nullable=True),
        sa.Column("last_failed_at", sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.operator_id"]),
        sa.PrimaryKeyConstraint("operator_id"),
    )


def downgrade() -> None:
    op.drop_table("login_throttle_states")
    op.drop_table("revoked_tokens")
    op.drop_table("operators")
