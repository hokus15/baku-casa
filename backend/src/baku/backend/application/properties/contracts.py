"""Application-layer contracts (internal DTOs) for the properties module — F-0003."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from baku.backend.domain.properties.enums import (
    AcquisitionType,
    FiscalNature,
    FiscalSituation,
    PropertyType,
)


@dataclass
class OwnershipInput:
    """Input DTO for a single ownership entry on create/replace."""

    owner_id: str
    ownership_percentage: Decimal


@dataclass
class CreatePropertyCommand:
    """Command for the create_property use case."""

    name: str
    type: PropertyType
    created_by: str
    ownerships: list[OwnershipInput]
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


@dataclass
class UpdatePropertyCommand:
    """Command for the update_property use case. None means 'no change'."""

    property_id: str
    updated_by: str
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


@dataclass
class ReplaceOwnershipCommand:
    """Command for the replace_property_ownership use case."""

    property_id: str
    ownerships: list[OwnershipInput]
    updated_by: str


@dataclass
class DeletePropertyCommand:
    """Command for the delete_property use case."""

    property_id: str
    deleted_by: str


@dataclass
class OwnershipResult:
    """Result DTO for a single ownership record."""

    property_id: str
    owner_id: str
    ownership_percentage: Decimal
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    deleted_at: datetime | None
    deleted_by: str | None


@dataclass
class PropertyResult:
    """Result DTO for a property with its current active ownerships."""

    property_id: str
    name: str
    type: PropertyType
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    ownerships: list[OwnershipResult]
    description: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    province: str | None = None
    country: str | None = None
    cadastral_reference: str | None = None
    cadastral_value: Decimal | None = None
    cadastral_land_value: Decimal | None = None
    cadastral_construction_value: Decimal | None = None
    construction_ratio: Decimal | None = None
    cadastral_value_revised: bool | None = None
    acquisition_date: date | None = None
    acquisition_type: AcquisitionType | None = None
    transfer_date: date | None = None
    transfer_type: AcquisitionType | None = None
    fiscal_nature: FiscalNature | None = None
    fiscal_situation: FiscalSituation | None = None
    deleted_at: datetime | None = None
    deleted_by: str | None = None


@dataclass
class PropertyListResult:
    """Paginated list of property results."""

    items: list[PropertyResult]
    total: int
    page: int
    page_size: int
