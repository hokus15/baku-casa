"""Use case: UpdateOwner — edit an active owner's mutable fields.

Raises:
  OwnerNotFound       — owner does not exist or is already deleted.
  OwnerTaxIdConflict  — new tax_id (normalized) conflicts with another active owner.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.owners.entities import Owner
from baku.backend.domain.owners.errors import OwnerNotFound, OwnerTaxIdConflict
from baku.backend.domain.owners.repositories import OwnerRepository, OwnerUnitOfWorkPort
from baku.backend.domain.owners.tax_id_normalizer import normalize_tax_id
from baku.backend.domain.owners.value_objects import EntityType

logger = logging.getLogger(__name__)


class _Unset:
    """Sentinel for fields not provided in PATCH payload."""

    _instance: "_Unset | None" = None

    def __new__(cls) -> "_Unset":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "UNSET"


UNSET: Any = _Unset()


@dataclass
class OwnerUpdate:
    """Fields to update. UNSET sentinel means the field was not provided."""

    entity_type: Any = field(default=UNSET)
    first_name: Any = field(default=UNSET)
    last_name: Any = field(default=UNSET)
    legal_name: Any = field(default=UNSET)
    raw_tax_id: Any = field(default=UNSET)
    fiscal_address_line1: Any = field(default=UNSET)
    fiscal_address_city: Any = field(default=UNSET)
    fiscal_address_postal_code: Any = field(default=UNSET)
    fiscal_address_country: Any = field(default=UNSET)
    email: Any = field(default=UNSET)
    land_line: Any = field(default=UNSET)
    land_line_country_code: Any = field(default=UNSET)
    mobile: Any = field(default=UNSET)
    mobile_country_code: Any = field(default=UNSET)
    stamp_image: Any = field(default=UNSET)

    @staticmethod
    def from_provided(provided: set[str], **kwargs: Any) -> "OwnerUpdate":
        """Build patch from a set of field names that were actually in the request."""
        patch = OwnerUpdate(
        """Build patch from a set of field names that were actually in the request."""
        patch = OwnerUpdate(
            entity_type=kwargs.get("entity_type", UNSET) if "entity_type" in provided else UNSET,
            first_name=kwargs.get("first_name", UNSET) if "first_name" in provided else UNSET,
            last_name=kwargs.get("last_name", UNSET) if "last_name" in provided else UNSET,
            legal_name=kwargs.get("legal_name", UNSET) if "legal_name" in provided else UNSET,
            raw_tax_id=kwargs.get("tax_id", UNSET) if "tax_id" in provided else UNSET,
            fiscal_address_line1=(
                kwargs.get("fiscal_address_line1", UNSET) if "fiscal_address_line1" in provided else UNSET
            ),
            fiscal_address_city=(
                kwargs.get("fiscal_address_city", UNSET) if "fiscal_address_city" in provided else UNSET
            ),
            fiscal_address_postal_code=(
                kwargs.get("fiscal_address_postal_code", UNSET) if "fiscal_address_postal_code" in provided else UNSET
            ),
            fiscal_address_country=(
                kwargs.get("fiscal_address_country", UNSET) if "fiscal_address_country" in provided else UNSET
            ),
            email=kwargs.get("email", UNSET) if "email" in provided else UNSET,
            land_line=kwargs.get("land_line", UNSET) if "land_line" in provided else UNSET,
            land_line_country_code=(
                kwargs.get("land_line_country_code", UNSET) if "land_line_country_code" in provided else UNSET
            ),
            mobile=kwargs.get("mobile", UNSET) if "mobile" in provided else UNSET,
            mobile_country_code=(
                kwargs.get("mobile_country_code", UNSET) if "mobile_country_code" in provided else UNSET
            ),
            stamp_image=kwargs.get("stamp_image", UNSET) if "stamp_image" in provided else UNSET,
        )
        return patch

    def is_provided(self, value: Any) -> bool:
        return not isinstance(value, _Unset)


def update_owner(
    owner_id: str,
    updated_by: str,
    patch: OwnerUpdate,
    owner_repo: OwnerRepository,
    uow: OwnerUnitOfWorkPort,
) -> Owner:
    logger.info(
        "update_owner_started",
        extra={"operation": "update_owner", "owner_id": owner_id},
    )
    owner = owner_repo.find_by_id(owner_id, include_deleted=False)
    if owner is None:
        raise OwnerNotFound()

    if patch.is_provided(patch.raw_tax_id):
        normalized_tax_id = normalize_tax_id(patch.raw_tax_id)
        conflict = owner_repo.find_by_tax_id(normalized_tax_id, exclude_owner_id=owner_id)
        if conflict is not None:
            raise OwnerTaxIdConflict()
        owner.tax_id = normalized_tax_id

    if patch.is_provided(patch.entity_type):
        owner.entity_type = EntityType(patch.entity_type)
    if patch.is_provided(patch.first_name):
        owner.first_name = patch.first_name
    if patch.is_provided(patch.last_name):
        owner.last_name = patch.last_name
    if patch.is_provided(patch.legal_name):
        owner.legal_name = patch.legal_name
    if patch.is_provided(patch.fiscal_address_line1):
        owner.fiscal_address_line1 = patch.fiscal_address_line1
    if patch.is_provided(patch.fiscal_address_city):
        owner.fiscal_address_city = patch.fiscal_address_city
    if patch.is_provided(patch.fiscal_address_postal_code):
        owner.fiscal_address_postal_code = patch.fiscal_address_postal_code
    if patch.is_provided(patch.fiscal_address_country):
        owner.fiscal_address_country = patch.fiscal_address_country
    if patch.is_provided(patch.email):
        owner.email = patch.email or None
    if patch.is_provided(patch.land_line):
        owner.land_line = patch.land_line or None
    if patch.is_provided(patch.land_line_country_code):
        owner.land_line_country_code = patch.land_line_country_code
    if patch.is_provided(patch.mobile):
        owner.mobile = patch.mobile or None
    if patch.is_provided(patch.mobile_country_code):
        owner.mobile_country_code = patch.mobile_country_code
    if patch.is_provided(patch.stamp_image):
        owner.stamp_image = patch.stamp_image or None

    owner.updated_at = utcnow()
    owner.updated_by = updated_by

    owner_repo.save(owner)
    uow.commit()

    logger.info(
        "update_owner_completed",
        extra={"operation": "update_owner", "owner_id": owner_id},
    )
    return owner
