"""HTTP schemas (DTOs) for properties endpoints — F-0003.

All field names are in English to match the domain model.
Decimal fields (ownership_percentage, cadastral values) are serialized as strings.
Null optional fields are excluded from responses (response_model_exclude_none=True).
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator, model_validator

from baku.backend.domain.properties.enums import (
    AcquisitionType,
    FiscalNature,
    FiscalSituation,
    PropertyType,
)


class OwnershipInputSchema(BaseModel):
    owner_id: str
    ownership_percentage: Decimal

    @field_validator("owner_id")
    @classmethod
    def _owner_id_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("owner_id must not be blank.")
        return v

    @field_validator("ownership_percentage", mode="before")
    @classmethod
    def _parse_percentage(cls, v: object) -> Decimal:
        if isinstance(v, str):
            return Decimal(v)
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return v  # type: ignore[return-value]


class CreatePropertyRequest(BaseModel):
    name: str
    type: PropertyType
    ownerships: list[OwnershipInputSchema]
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

    @field_validator("name")
    @classmethod
    def _name_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("name must not be blank.")
        return v

    @model_validator(mode="after")
    def _at_least_one_ownership(self) -> "CreatePropertyRequest":
        if not self.ownerships:
            from baku.backend.domain.properties.errors import (
                PropertyOwnershipRequired,
            )

            raise PropertyOwnershipRequired()
        return self

    model_config = {"from_attributes": True}


class UpdatePropertyRequest(BaseModel):
    name: str | None = None
    type: PropertyType | None = None
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

    model_config = {"from_attributes": True}


class ReplaceOwnershipRequest(BaseModel):
    ownerships: list[OwnershipInputSchema]

    @model_validator(mode="after")
    def _at_least_one_ownership(self) -> "ReplaceOwnershipRequest":
        if not self.ownerships:
            from baku.backend.domain.properties.errors import (
                PropertyOwnershipRequired,
            )

            raise PropertyOwnershipRequired()
        return self

    model_config = {"from_attributes": True}


class OwnershipResponse(BaseModel):
    property_id: str
    owner_id: str
    ownership_percentage: str
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    deleted_at: datetime | None = None
    deleted_by: str | None = None

    model_config = {"from_attributes": True}

    @field_validator("ownership_percentage", mode="before")
    @classmethod
    def _decimal_to_str(cls, v: object) -> str:
        if isinstance(v, Decimal):
            return f"{v:.2f}"
        return str(v)


class PropertyResponse(BaseModel):
    property_id: str
    name: str
    type: PropertyType
    ownerships: list[OwnershipResponse]
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
    cadastral_value: str | None = None
    cadastral_land_value: str | None = None
    cadastral_construction_value: str | None = None
    construction_ratio: str | None = None
    cadastral_value_revised: bool | None = None
    acquisition_date: date | None = None
    acquisition_type: AcquisitionType | None = None
    transfer_date: date | None = None
    transfer_type: AcquisitionType | None = None
    fiscal_nature: FiscalNature | None = None
    fiscal_situation: FiscalSituation | None = None
    deleted_at: datetime | None = None
    deleted_by: str | None = None

    model_config = {"from_attributes": True}

    @field_validator(
        "cadastral_value",
        "cadastral_land_value",
        "cadastral_construction_value",
        "construction_ratio",
        mode="before",
    )
    @classmethod
    def _decimal_to_str(cls, v: object) -> str | None:
        if v is None:
            return None
        if isinstance(v, Decimal):
            return f"{v:.2f}"
        return str(v)


class PropertyListResponse(BaseModel):
    items: list[PropertyResponse]
    total: int
    page: int
    page_size: int

    model_config = {"from_attributes": True}


class OwnershipListResponse(BaseModel):
    items: list[OwnershipResponse]
    total: int
    page: int
    page_size: int
