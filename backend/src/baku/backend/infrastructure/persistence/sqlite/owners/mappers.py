"""ORM <-> domain mappers for owners — infrastructure layer.

Datetime fields are persisted as ISO 8601 UTC strings (same pattern as auth).
"""

from __future__ import annotations

from datetime import datetime, timezone

from baku.backend.domain.owners.entities import Owner
from baku.backend.domain.owners.value_objects import EntityType
from baku.backend.infrastructure.persistence.sqlite.owners.models import OwnerORM


def _dt_to_str(dt: datetime) -> str:
    return dt.isoformat()


def _str_to_dt(s: str) -> datetime:
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def orm_to_owner(row: OwnerORM) -> Owner:
    return Owner(
        owner_id=row.owner_id,
        entity_type=EntityType(row.entity_type),
        first_name=row.first_name,
        last_name=row.last_name,
        legal_name=row.legal_name,
        tax_id=row.tax_id,
        fiscal_address_line1=row.fiscal_address_line1,
        fiscal_address_city=row.fiscal_address_city,
        fiscal_address_postal_code=row.fiscal_address_postal_code,
        fiscal_address_country=row.fiscal_address_country,
        email=row.email,
        land_line=row.land_line,
        land_line_country_code=row.land_line_country_code,
        mobile=row.mobile,
        mobile_country_code=row.mobile_country_code,
        stamp_image=row.stamp_image,
        created_at=_str_to_dt(row.created_at),
        created_by=row.created_by,
        updated_at=_str_to_dt(row.updated_at),
        updated_by=row.updated_by,
        deleted_at=_str_to_dt(row.deleted_at) if row.deleted_at else None,
        deleted_by=row.deleted_by,
    )


def owner_to_orm(owner: Owner, row: OwnerORM | None = None) -> OwnerORM:
    if row is None:
        row = OwnerORM(owner_id=owner.owner_id)
    row.entity_type = owner.entity_type.value
    row.first_name = owner.first_name
    row.last_name = owner.last_name
    row.legal_name = owner.legal_name
    row.tax_id = owner.tax_id
    row.fiscal_address_line1 = owner.fiscal_address_line1
    row.fiscal_address_city = owner.fiscal_address_city
    row.fiscal_address_postal_code = owner.fiscal_address_postal_code
    row.fiscal_address_country = owner.fiscal_address_country
    row.email = owner.email
    row.land_line = owner.land_line
    row.land_line_country_code = owner.land_line_country_code
    row.mobile = owner.mobile
    row.mobile_country_code = owner.mobile_country_code
    row.stamp_image = owner.stamp_image
    row.created_at = _dt_to_str(owner.created_at)
    row.created_by = owner.created_by
    row.updated_at = _dt_to_str(owner.updated_at)
    row.updated_by = owner.updated_by
    row.deleted_at = _dt_to_str(owner.deleted_at) if owner.deleted_at else None
    row.deleted_by = owner.deleted_by
    return row
