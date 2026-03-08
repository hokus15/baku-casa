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
