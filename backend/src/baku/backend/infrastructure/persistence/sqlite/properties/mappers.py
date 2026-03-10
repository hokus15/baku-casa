"""ORM <-> domain mappers for properties and ownerships — infrastructure layer.

Datetime fields are persisted as ISO 8601 UTC strings.
Decimal fields (ownership_percentage, cadastral values) are persisted as strings.
Date-only fields (acquisition_date, transfer_date) are persisted as YYYY-MM-DD strings.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from baku.backend.domain.properties.entities import Ownership, Property
from baku.backend.domain.properties.enums import (
    AcquisitionType,
    FiscalNature,
    FiscalSituation,
    PropertyType,
)
from baku.backend.infrastructure.persistence.sqlite.properties.models import (
    OwnershipORM,
    PropertyORM,
)


def _dt_to_str(dt: datetime) -> str:
    return dt.isoformat()


def _str_to_dt(s: str) -> datetime:
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _date_to_str(d: date) -> str:
    return d.isoformat()


def _str_to_date(s: str) -> date:
    return date.fromisoformat(s)


def orm_to_property(row: PropertyORM) -> Property:
    return Property(
        property_id=row.property_id,
        name=row.name,
        type=PropertyType(row.type),
        description=row.description,
        address=row.address,
        city=row.city,
        postal_code=row.postal_code,
        province=row.province,
        country=row.country,
        cadastral_reference=row.cadastral_reference,
        cadastral_value=(
            Decimal(row.cadastral_value) if row.cadastral_value else None
        ),
        cadastral_land_value=(
            Decimal(row.cadastral_land_value)
            if row.cadastral_land_value
            else None
        ),
        cadastral_value_revised=(
            (row.cadastral_value_revised == "true")
            if row.cadastral_value_revised
            else None
        ),
        acquisition_date=(
            _str_to_date(row.acquisition_date)
            if row.acquisition_date
            else None
        ),
        acquisition_type=(
            AcquisitionType(row.acquisition_type)
            if row.acquisition_type
            else None
        ),
        transfer_date=(
            _str_to_date(row.transfer_date) if row.transfer_date else None
        ),
        transfer_type=(
            AcquisitionType(row.transfer_type) if row.transfer_type else None
        ),
        fiscal_nature=(
            FiscalNature(row.fiscal_nature) if row.fiscal_nature else None
        ),
        fiscal_situation=(
            FiscalSituation(row.fiscal_situation)
            if row.fiscal_situation
            else None
        ),
        created_at=_str_to_dt(row.created_at),
        created_by=row.created_by,
        updated_at=_str_to_dt(row.updated_at),
        updated_by=row.updated_by,
        deleted_at=_str_to_dt(row.deleted_at) if row.deleted_at else None,
        deleted_by=row.deleted_by,
    )


def property_to_orm(
    property_: Property, row: PropertyORM | None = None
) -> PropertyORM:
    if row is None:
        row = PropertyORM(property_id=property_.property_id)
    row.name = property_.name
    row.type = property_.type.value
    row.description = property_.description
    row.address = property_.address
    row.city = property_.city
    row.postal_code = property_.postal_code
    row.province = property_.province
    row.country = property_.country
    row.cadastral_reference = property_.cadastral_reference
    row.cadastral_value = (
        str(property_.cadastral_value)
        if property_.cadastral_value is not None
        else None
    )
    row.cadastral_land_value = (
        str(property_.cadastral_land_value)
        if property_.cadastral_land_value is not None
        else None
    )
    row.cadastral_value_revised = (
        "true"
        if property_.cadastral_value_revised is True
        else "false" if property_.cadastral_value_revised is False else None
    )
    row.acquisition_date = (
        _date_to_str(property_.acquisition_date)
        if property_.acquisition_date
        else None
    )
    row.acquisition_type = (
        property_.acquisition_type.value
        if property_.acquisition_type
        else None
    )
    row.transfer_date = (
        _date_to_str(property_.transfer_date)
        if property_.transfer_date
        else None
    )
    row.transfer_type = (
        property_.transfer_type.value if property_.transfer_type else None
    )
    row.fiscal_nature = (
        property_.fiscal_nature.value if property_.fiscal_nature else None
    )
    row.fiscal_situation = (
        property_.fiscal_situation.value
        if property_.fiscal_situation
        else None
    )
    row.created_at = _dt_to_str(property_.created_at)
    row.created_by = property_.created_by
    row.updated_at = _dt_to_str(property_.updated_at)
    row.updated_by = property_.updated_by
    row.deleted_at = (
        _dt_to_str(property_.deleted_at) if property_.deleted_at else None
    )
    row.deleted_by = property_.deleted_by
    return row


def orm_to_ownership(row: OwnershipORM) -> Ownership:
    return Ownership(
        ownership_id=row.ownership_id,
        property_id=row.property_id,
        owner_id=row.owner_id,
        ownership_percentage=Decimal(row.ownership_percentage),
        created_at=_str_to_dt(row.created_at),
        created_by=row.created_by,
        updated_at=_str_to_dt(row.updated_at),
        updated_by=row.updated_by,
        deleted_at=_str_to_dt(row.deleted_at) if row.deleted_at else None,
        deleted_by=row.deleted_by,
    )


def ownership_to_orm(
    ownership: Ownership, row: OwnershipORM | None = None
) -> OwnershipORM:
    if row is None:
        row = OwnershipORM(ownership_id=ownership.ownership_id)
    row.property_id = ownership.property_id
    row.owner_id = ownership.owner_id
    row.ownership_percentage = str(ownership.ownership_percentage)
    row.created_at = _dt_to_str(ownership.created_at)
    row.created_by = ownership.created_by
    row.updated_at = _dt_to_str(ownership.updated_at)
    row.updated_by = ownership.updated_by
    row.deleted_at = (
        _dt_to_str(ownership.deleted_at) if ownership.deleted_at else None
    )
    row.deleted_by = ownership.deleted_by
    return row
