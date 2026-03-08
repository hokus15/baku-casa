"""HTTP schemas (DTOs) for owners endpoints — F-0002.

All field names are in English to match the domain model.
Serialization of datetimes uses ISO 8601 UTC strings.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_validator

from baku.backend.domain.owners.value_objects import EntityType


class OwnerCreateRequest(BaseModel):
    entity_type: EntityType
    first_name: str
    last_name: str
    legal_name: str
    tax_id: str
    fiscal_address_line1: str
    fiscal_address_city: str
    fiscal_address_postal_code: str
    fiscal_address_country: str = "ES"
    email: str | None = None
    land_line: str | None = None
    land_line_country_code: int | None = None
    mobile: str | None = None
    mobile_country_code: int | None = None
    stamp_image: str | None = None

    @field_validator(
        "first_name",
        "last_name",
        "legal_name",
        "tax_id",
        "fiscal_address_line1",
        "fiscal_address_city",
        "fiscal_address_postal_code",
    )
    @classmethod
    def _not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be blank.")
        return v


class OwnerUpdateRequest(BaseModel):
    entity_type: EntityType | None = None
    first_name: str | None = None
    last_name: str | None = None
    legal_name: str | None = None
    tax_id: str | None = None
    fiscal_address_line1: str | None = None
    fiscal_address_city: str | None = None
    fiscal_address_postal_code: str | None = None
    fiscal_address_country: str | None = None
    email: str | None = None
    land_line: str | None = None
    land_line_country_code: int | None = None
    mobile: str | None = None
    mobile_country_code: int | None = None
    stamp_image: str | None = None


class OwnerResponse(BaseModel):
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
    email: str | None
    land_line: str | None
    land_line_country_code: int | None
    mobile: str | None
    mobile_country_code: int | None
    stamp_image: str | None
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    deleted_at: datetime | None
    deleted_by: str | None

    model_config = {"from_attributes": True}


class OwnerListResponse(BaseModel):
    items: list[OwnerResponse]
    total: int
    page: int
    page_size: int
