"""SQLAlchemy ORM models for properties and ownerships — infrastructure layer only.

Domain entities (entities.py) must NOT import from this module.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from baku.backend.infrastructure.persistence.sqlite.orm_models import Base


class PropertyORM(Base):
    __tablename__ = "properties"
    __table_args__ = (Index("ix_properties_deleted_at", "deleted_at"),)

    property_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True
    )
    address: Mapped[str | None] = mapped_column(String(512), nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    province: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(2), nullable=True)
    cadastral_reference: Mapped[str | None] = mapped_column(
        String(25), nullable=True
    )
    cadastral_value: Mapped[str | None] = mapped_column(
        String(32), nullable=True
    )
    cadastral_land_value: Mapped[str | None] = mapped_column(
        String(32), nullable=True
    )
    cadastral_value_revised: Mapped[str | None] = mapped_column(
        String(5), nullable=True
    )
    acquisition_date: Mapped[str | None] = mapped_column(
        String(10), nullable=True
    )
    acquisition_type: Mapped[str | None] = mapped_column(
        String(16), nullable=True
    )
    transfer_date: Mapped[str | None] = mapped_column(
        String(10), nullable=True
    )
    transfer_type: Mapped[str | None] = mapped_column(
        String(16), nullable=True
    )
    fiscal_nature: Mapped[str | None] = mapped_column(
        String(16), nullable=True
    )
    fiscal_situation: Mapped[str | None] = mapped_column(
        String(32), nullable=True
    )
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_by: Mapped[str] = mapped_column(String(255), nullable=False)
    deleted_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    deleted_by: Mapped[str | None] = mapped_column(String(255), nullable=True)


class OwnershipORM(Base):
    __tablename__ = "ownerships"
    __table_args__ = (
        # Active-pair uniqueness (property_id, owner_id, deleted_at IS NULL) is enforced
        # at the application layer since partial unique indexes require dialect-specific SQL.
        # These indexes accelerate the most common lookup patterns.
        Index("ix_ownerships_property_id", "property_id"),
        Index("ix_ownerships_owner_id", "owner_id"),
        Index("ix_ownerships_deleted_at", "deleted_at"),
    )

    ownership_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    property_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("properties.property_id", ondelete="RESTRICT"),
        nullable=False,
    )
    owner_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("owners.owner_id"),
        nullable=False,
    )
    ownership_percentage: Mapped[str] = mapped_column(
        String(32), nullable=False
    )
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_by: Mapped[str] = mapped_column(String(255), nullable=False)
    deleted_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    deleted_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
