"""Use case: CreateOwner — create a new owner with validation and tax_id uniqueness.

Raises:
  OwnerValidationError  — required fields are blank or invalid.
  OwnerTaxIdConflict    — an active owner with the same normalized tax_id already exists.
"""

from __future__ import annotations

import logging

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.owners.entities import Owner
from baku.backend.domain.owners.errors import OwnerTaxIdConflict, OwnerValidationError
from baku.backend.domain.owners.repositories import OwnerRepository, OwnerUnitOfWorkPort
from baku.backend.domain.owners.tax_id_normalizer import normalize_tax_id
from baku.backend.domain.owners.value_objects import EntityType

logger = logging.getLogger(__name__)


def create_owner(
    entity_type: EntityType,
    first_name: str,
    last_name: str,
    legal_name: str,
    raw_tax_id: str,
    fiscal_address_line1: str,
    fiscal_address_city: str,
    fiscal_address_postal_code: str,
    fiscal_address_country: str,
    created_by: str,
    owner_repo: OwnerRepository,
    uow: OwnerUnitOfWorkPort,
    email: str | None = None,
    land_line: str | None = None,
    land_line_country_code: int | None = None,
    mobile: str | None = None,
    mobile_country_code: int | None = None,
    stamp_image: str | None = None,
) -> Owner:
    normalized_tax_id = normalize_tax_id(raw_tax_id)
    if not normalized_tax_id:
        raise OwnerValidationError("tax_id must not be blank after normalization.")

    logger.info(
        "create_owner_started",
        extra={"operation": "create_owner"},
    )

    existing = owner_repo.find_by_tax_id(normalized_tax_id)
    if existing is not None:
        raise OwnerTaxIdConflict()

    now = utcnow()
    owner = Owner.new(
        entity_type=entity_type,
        first_name=first_name,
        last_name=last_name,
        legal_name=legal_name,
        tax_id=normalized_tax_id,
        fiscal_address_line1=fiscal_address_line1,
        fiscal_address_city=fiscal_address_city,
        fiscal_address_postal_code=fiscal_address_postal_code,
        fiscal_address_country=fiscal_address_country,
        created_by=created_by,
        now=now,
        email=email,
        land_line=land_line,
        land_line_country_code=land_line_country_code,
        mobile=mobile,
        mobile_country_code=mobile_country_code,
        stamp_image=stamp_image,
    )
    owner_repo.save(owner)
    uow.commit()

    logger.info(
        "create_owner_completed",
        extra={"operation": "create_owner", "owner_id": owner.owner_id},
    )
    return owner
