"""Use case: CreateProperty — create a new property with initial ownership.

Raises:
    PropertyOwnershipRequired  — no ownership entries provided.
    PropertyValidationError    — name is blank or percentage precision/range invalid.
    OwnerNotFoundForOwnership  — referenced owner_id does not exist or is deleted.
    OwnershipDuplicateActivePair — duplicate owner_id in the request.
    PropertyOwnershipSumExceeded — ownership percentages sum exceeds 100.
"""

from __future__ import annotations

import logging

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.application.properties.contracts import (
    CreatePropertyCommand,
    OwnershipResult,
    PropertyResult,
)
from baku.backend.domain.owners.repositories import OwnerRepository
from baku.backend.domain.properties.entities import Ownership, Property
from baku.backend.domain.properties.errors import (
    OwnerNotFoundForOwnership,
    PropertyOwnershipRequired,
    PropertyValidationError,
)
from baku.backend.domain.properties.policies import validate_ownership_inputs
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)

logger = logging.getLogger(__name__)


def create_property(
    cmd: CreatePropertyCommand,
    property_repo: PropertyRepository,
    ownership_repo: OwnershipRepository,
    owner_repo: OwnerRepository,
    uow: PropertyUnitOfWorkPort,
) -> PropertyResult:
    """Create a new property with at least one ownership record."""

    if not cmd.name or not cmd.name.strip():
        raise PropertyValidationError("name must not be blank.")

    if not cmd.ownerships:
        raise PropertyOwnershipRequired()

    # Validate ownership inputs (percentage precision, sum, uniqueness)
    validate_ownership_inputs(
        [(o.owner_id, o.ownership_percentage) for o in cmd.ownerships]
    )

    # Verify each referenced owner exists and is active
    for o in cmd.ownerships:
        owner = owner_repo.find_by_id(o.owner_id)
        if owner is None:
            raise OwnerNotFoundForOwnership(
                f"Owner '{o.owner_id}' not found or has been deleted."
            )

    logger.info(
        "create_property_started",
        extra={"operation": "create_property"},
    )

    now = utcnow()

    try:
        property_ = Property.new(
            name=cmd.name,
            type=cmd.type,
            created_by=cmd.created_by,
            now=now,
            description=cmd.description,
            address=cmd.address,
            city=cmd.city,
            postal_code=cmd.postal_code,
            province=cmd.province,
            country=cmd.country,
            cadastral_reference=cmd.cadastral_reference,
            cadastral_value=cmd.cadastral_value,
            cadastral_land_value=cmd.cadastral_land_value,
            cadastral_value_revised=cmd.cadastral_value_revised,
            acquisition_date=cmd.acquisition_date,
            acquisition_type=cmd.acquisition_type,
            transfer_date=cmd.transfer_date,
            transfer_type=cmd.transfer_type,
            fiscal_nature=cmd.fiscal_nature,
            fiscal_situation=cmd.fiscal_situation,
        )
    except ValueError as exc:
        raise PropertyValidationError(str(exc)) from exc
    property_repo.save(property_)

    ownerships = []
    for o in cmd.ownerships:
        ownership = Ownership.new(
            property_id=property_.property_id,
            owner_id=o.owner_id,
            ownership_percentage=o.ownership_percentage,
            created_by=cmd.created_by,
            now=now,
        )
        ownership_repo.save(ownership)
        ownerships.append(ownership)

    uow.commit()

    logger.info(
        "create_property_completed",
        extra={
            "operation": "create_property",
            "property_id": property_.property_id,
        },
    )

    return _to_result(property_, ownerships)


def _to_result(
    property_: Property, ownerships: list[Ownership]
) -> PropertyResult:
    ownership_results = [
        OwnershipResult(
            property_id=o.property_id,
            owner_id=o.owner_id,
            ownership_percentage=o.ownership_percentage,
            created_at=o.created_at,
            created_by=o.created_by,
            updated_at=o.updated_at,
            updated_by=o.updated_by,
            deleted_at=o.deleted_at,
            deleted_by=o.deleted_by,
        )
        for o in ownerships
    ]
    return PropertyResult(
        property_id=property_.property_id,
        name=property_.name,
        type=property_.type,
        ownerships=ownership_results,
        description=property_.description,
        address=property_.address,
        city=property_.city,
        postal_code=property_.postal_code,
        province=property_.province,
        country=property_.country,
        cadastral_reference=property_.cadastral_reference,
        cadastral_value=property_.cadastral_value,
        cadastral_land_value=property_.cadastral_land_value,
        cadastral_construction_value=property_.cadastral_construction_value,
        construction_ratio=property_.construction_ratio,
        cadastral_value_revised=property_.cadastral_value_revised,
        acquisition_date=property_.acquisition_date,
        acquisition_type=property_.acquisition_type,
        transfer_date=property_.transfer_date,
        transfer_type=property_.transfer_type,
        fiscal_nature=property_.fiscal_nature,
        fiscal_situation=property_.fiscal_situation,
        created_at=property_.created_at,
        created_by=property_.created_by,
        updated_at=property_.updated_at,
        updated_by=property_.updated_by,
        deleted_at=property_.deleted_at,
        deleted_by=property_.deleted_by,
    )
