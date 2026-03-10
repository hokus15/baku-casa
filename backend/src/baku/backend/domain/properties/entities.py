"""Property and Ownership domain entities — pure Python, no framework dependencies.

Invariants enforced:
- property_id and ownership pair (property_id, owner_id) are immutable after creation.
- Audit timestamps are always UTC-aware.
- deleted_by is required when deleted_at is set.
- Soft-deleted entities cannot be edited.
- cadastral_construction_value = cadastral_value - cadastral_land_value (when both present).
- construction_ratio = (cadastral_construction_value / cadastral_value) * 100 (when applicable).
- cadastral_construction_value >= 0 (cadastral_land_value must not exceed cadastral_value).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from baku.backend.domain.properties.enums import (
    AcquisitionType,
    FiscalNature,
    FiscalSituation,
    PropertyType,
)
from baku.backend.domain.properties.value_objects import (
    validate_ownership_percentage,
)


@dataclass
class Property:
    """Immovable asset managed by the authenticated operator."""

    property_id: str
    name: str
    type: PropertyType
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    description: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    province: str | None = None
    country: str | None = None
    cadastral_reference: str | None = None
    cadastral_value: Decimal | None = None
    cadastral_land_value: Decimal | None = None
    cadastral_value_revised: bool | None = None
    acquisition_date: date | None = None
    acquisition_type: AcquisitionType | None = None
    transfer_date: date | None = None
    transfer_type: AcquisitionType | None = None
    fiscal_nature: FiscalNature | None = None
    fiscal_situation: FiscalSituation | None = None
    deleted_at: datetime | None = None
    deleted_by: str | None = None

    def __post_init__(self) -> None:
        if not self.property_id or not self.property_id.strip():
            raise ValueError("property_id must not be blank.")
        if not self.name or not self.name.strip():
            raise ValueError("name must not be blank.")
        self._require_utc_aware(self.created_at, "created_at")
        self._require_utc_aware(self.updated_at, "updated_at")
        if self.deleted_at is not None:
            self._require_utc_aware(self.deleted_at, "deleted_at")
            if not self.deleted_by or not self.deleted_by.strip():
                raise ValueError(
                    "deleted_by is required when deleted_at is set."
                )
        if (
            self.cadastral_value is not None
            and self.cadastral_value < Decimal("0")
        ):
            raise ValueError("cadastral_value must be >= 0.")
        if (
            self.cadastral_land_value is not None
            and self.cadastral_land_value < Decimal("0")
        ):
            raise ValueError("cadastral_land_value must be >= 0.")
        if (
            self.cadastral_value is not None
            and self.cadastral_land_value is not None
            and self.cadastral_land_value > self.cadastral_value
        ):
            raise ValueError(
                "cadastral_land_value must not exceed cadastral_value "
                "(cadastral_construction_value would be negative)."
            )

    @staticmethod
    def _require_utc_aware(dt: datetime, name: str) -> None:
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            raise ValueError(f"{name} must be UTC-aware.")

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @property
    def cadastral_construction_value(self) -> Decimal | None:
        """Derived: cadastral_value - cadastral_land_value (when both values exist)."""
        if (
            self.cadastral_value is not None
            and self.cadastral_land_value is not None
        ):
            return self.cadastral_value - self.cadastral_land_value
        return None

    @property
    def construction_ratio(self) -> Decimal | None:
        """Derived: (construction / cadastral_value) * 100.

        Returns None when cadastral_value is 0, None, or construction is not derivable.
        """
        construction = self.cadastral_construction_value
        if construction is None:
            return None
        if self.cadastral_value is None or self.cadastral_value == Decimal(
            "0"
        ):
            return None
        return (construction / self.cadastral_value) * Decimal("100")

    @staticmethod
    def new(
        name: str,
        type: PropertyType,
        created_by: str,
        now: datetime,
        description: str | None = None,
        address: str | None = None,
        city: str | None = None,
        postal_code: str | None = None,
        province: str | None = None,
        country: str | None = None,
        cadastral_reference: str | None = None,
        cadastral_value: Decimal | None = None,
        cadastral_land_value: Decimal | None = None,
        cadastral_value_revised: bool | None = None,
        acquisition_date: date | None = None,
        acquisition_type: AcquisitionType | None = None,
        transfer_date: date | None = None,
        transfer_type: AcquisitionType | None = None,
        fiscal_nature: FiscalNature | None = None,
        fiscal_situation: FiscalSituation | None = None,
    ) -> "Property":
        property_id = str(uuid.uuid4())
        return Property(
            property_id=property_id,
            name=name,
            type=type,
            created_at=now,
            created_by=created_by,
            updated_at=now,
            updated_by=created_by,
            description=description,
            address=address,
            city=city,
            postal_code=postal_code,
            province=province,
            country=country,
            cadastral_reference=cadastral_reference,
            cadastral_value=cadastral_value,
            cadastral_land_value=cadastral_land_value,
            cadastral_value_revised=cadastral_value_revised,
            acquisition_date=acquisition_date,
            acquisition_type=acquisition_type,
            transfer_date=transfer_date,
            transfer_type=transfer_type,
            fiscal_nature=fiscal_nature,
            fiscal_situation=fiscal_situation,
        )


@dataclass
class Ownership:
    """Active ownership relationship between a property and an owner (F-0002)."""

    ownership_id: str
    property_id: str
    owner_id: str
    ownership_percentage: Decimal
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    deleted_at: datetime | None = None
    deleted_by: str | None = None

    def __post_init__(self) -> None:
        if not self.ownership_id or not self.ownership_id.strip():
            raise ValueError("ownership_id must not be blank.")
        if not self.property_id or not self.property_id.strip():
            raise ValueError("property_id must not be blank.")
        if not self.owner_id or not self.owner_id.strip():
            raise ValueError("owner_id must not be blank.")
        validate_ownership_percentage(self.ownership_percentage)
        self._require_utc_aware(self.created_at, "created_at")
        self._require_utc_aware(self.updated_at, "updated_at")
        if self.deleted_at is not None:
            self._require_utc_aware(self.deleted_at, "deleted_at")
            if not self.deleted_by or not self.deleted_by.strip():
                raise ValueError(
                    "deleted_by is required when deleted_at is set."
                )

    @staticmethod
    def _require_utc_aware(dt: datetime, name: str) -> None:
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            raise ValueError(f"{name} must be UTC-aware.")

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @staticmethod
    def new(
        property_id: str,
        owner_id: str,
        ownership_percentage: Decimal,
        created_by: str,
        now: datetime,
    ) -> "Ownership":
        return Ownership(
            ownership_id=str(uuid.uuid4()),
            property_id=property_id,
            owner_id=owner_id,
            ownership_percentage=ownership_percentage,
            created_at=now,
            created_by=created_by,
            updated_at=now,
            updated_by=created_by,
        )
