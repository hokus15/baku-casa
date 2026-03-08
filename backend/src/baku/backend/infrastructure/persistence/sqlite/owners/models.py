"""SQLAlchemy ORM model for owners — infrastructure layer only.

Domain entities (entities.py) must NOT import from this module.
"""

from __future__ import annotations

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from baku.backend.infrastructure.persistence.sqlite.orm_models import Base


class OwnerORM(Base):
    __tablename__ = "owners"
    __table_args__ = (
        # Partial-like index: uniqueness of tax_id among active owners is enforced
        # at the application layer; this index accelerates tax_id lookup.
        Index("ix_owners_tax_id", "tax_id"),
        Index("ix_owners_deleted_at", "deleted_at"),
    )

    owner_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    legal_name: Mapped[str] = mapped_column(String(512), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(64), nullable=False)
    fiscal_address_line1: Mapped[str] = mapped_column(String(512), nullable=False)
    fiscal_address_city: Mapped[str] = mapped_column(String(255), nullable=False)
    fiscal_address_postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    fiscal_address_country: Mapped[str] = mapped_column(String(2), nullable=False, default="ES")
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    land_line: Mapped[str | None] = mapped_column(String(64), nullable=True)
    land_line_country_code: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(64), nullable=True)
    mobile_country_code: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    stamp_image: Mapped[str | None] = mapped_column(String(2097152), nullable=True)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_by: Mapped[str] = mapped_column(String(255), nullable=False)
    deleted_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    deleted_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
