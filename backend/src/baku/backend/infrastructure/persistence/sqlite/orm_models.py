"""SQLAlchemy ORM models for authentication — infrastructure layer only.

These models are explicit mappings of domain entities to DB tables.
Domain entities (entities.py) must NOT import from this module.
"""

from __future__ import annotations

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OperatorORM(Base):
    __tablename__ = "operators"
    __table_args__ = (
        # Enforces the single-operator invariant at DB level (ADR-0005, FR-001).
        # Only one row can ever satisfy singleton_guard = 1.
        UniqueConstraint("singleton_guard", name="uq_operators_singleton"),
        CheckConstraint("singleton_guard = 1", name="ck_operators_singleton_is_1"),
    )

    operator_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    credential_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    last_login_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # Always 1; the UNIQUE + CHECK constraints above prevent a second row.
    singleton_guard: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


class RevokedTokenORM(Base):
    __tablename__ = "revoked_tokens"

    token_jti: Mapped[str] = mapped_column(String(255), primary_key=True)
    operator_id: Mapped[str] = mapped_column(String(36), ForeignKey("operators.operator_id"), nullable=False)
    revoked_at: Mapped[str] = mapped_column(String(32), nullable=False)
    expires_at: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(String(32), nullable=False)


class LoginThrottleStateORM(Base):
    __tablename__ = "login_throttle_states"

    operator_id: Mapped[str] = mapped_column(String(36), ForeignKey("operators.operator_id"), primary_key=True)
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    blocked_until: Mapped[str | None] = mapped_column(String(32), nullable=True)
    last_failed_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
