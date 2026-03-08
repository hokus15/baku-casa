"""Owner domain entity — pure Python, no framework dependencies.

Invariants enforced:
- owner_id is immutable after creation.
- tax_id is stored in its normalized form.
- Audit timestamps are always UTC-aware.
- deleted_by is required when deleted_at is set.
- Soft-deleted owners cannot be edited.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from baku.backend.domain.owners.value_objects import EntityType


@dataclass
class Owner:
    """Fiscal subject managed by the authenticated operator."""

    owner_id: str
    entity_type: EntityType
    first_name: str
    last_name: str
    legal_name: str
    tax_id: str
    fiscal_address_line1: str
    fiscal_address_city: str
    fiscal_address_postal_code: str
    fiscal_address_country: str
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    email: str | None = None
    land_line: str | None = None
    land_line_country_code: int | None = None
    mobile: str | None = None
    mobile_country_code: int | None = None
    stamp_image: str | None = None
    deleted_at: datetime | None = None
    deleted_by: str | None = None

    def __post_init__(self) -> None:
        if not self.owner_id or not self.owner_id.strip():
            raise ValueError("owner_id must not be blank.")
        if not self.tax_id or not self.tax_id.strip():
            raise ValueError("tax_id must not be blank.")
        if not self.first_name or not self.first_name.strip():
            raise ValueError("first_name must not be blank.")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("last_name must not be blank.")
        if not self.legal_name or not self.legal_name.strip():
            raise ValueError("legal_name must not be blank.")
        if not self.fiscal_address_line1 or not self.fiscal_address_line1.strip():
            raise ValueError("fiscal_address_line1 must not be blank.")
        if not self.fiscal_address_city or not self.fiscal_address_city.strip():
            raise ValueError("fiscal_address_city must not be blank.")
        if not self.fiscal_address_postal_code or not self.fiscal_address_postal_code.strip():
            raise ValueError("fiscal_address_postal_code must not be blank.")
        if not self.fiscal_address_country or not self.fiscal_address_country.strip():
            raise ValueError("fiscal_address_country must not be blank.")
        self._require_utc_aware(self.created_at, "created_at")
        self._require_utc_aware(self.updated_at, "updated_at")
        if self.deleted_at is not None:
            self._require_utc_aware(self.deleted_at, "deleted_at")
            if not self.deleted_by or not self.deleted_by.strip():
                raise ValueError("deleted_by is required when deleted_at is set.")

    @staticmethod
    def _require_utc_aware(dt: datetime, name: str) -> None:
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            raise ValueError(f"{name} must be UTC-aware.")

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @staticmethod
    def new(
        entity_type: EntityType,
        first_name: str,
        last_name: str,
        legal_name: str,
        tax_id: str,
        fiscal_address_line1: str,
        fiscal_address_city: str,
        fiscal_address_postal_code: str,
        fiscal_address_country: str,
        created_by: str,
        now: datetime,
        email: str | None = None,
        land_line: str | None = None,
        land_line_country_code: int | None = None,
        mobile: str | None = None,
        mobile_country_code: int | None = None,
        stamp_image: str | None = None,
    ) -> "Owner":
        """Create a fresh owner. tax_id must already be normalized."""
        return Owner(
            owner_id=str(uuid.uuid4()),
            entity_type=entity_type,
            first_name=first_name,
            last_name=last_name,
            legal_name=legal_name,
            tax_id=tax_id,
            fiscal_address_line1=fiscal_address_line1,
            fiscal_address_city=fiscal_address_city,
            fiscal_address_postal_code=fiscal_address_postal_code,
            fiscal_address_country=fiscal_address_country,
            email=email or None,
            land_line=land_line or None,
            land_line_country_code=land_line_country_code,
            mobile=mobile or None,
            mobile_country_code=mobile_country_code,
            stamp_image=stamp_image or None,
            created_at=now,
            created_by=created_by,
            updated_at=now,
            updated_by=created_by,
        )
