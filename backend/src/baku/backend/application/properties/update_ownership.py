"""Use case: ReplacePropertyOwnership — replace existing ownership set — F-0003 US3.

Soft-deletes all active ownerships for the property and creates new ones.

Raises:
    PropertyNotFound — property_id does not exist or is soft-deleted.
    PropertyOwnershipRequired — no ownership entries provided.
    PropertyValidationError — percentage out of range or precision exceeded.
    OwnerNotFoundForOwnership — referenced owner_id does not exist.
    OwnershipDuplicateActivePair — duplicate owner_id in the new ownership list.
    PropertyOwnershipSumExceeded — new ownership percentages exceed 100.
"""

from __future__ import annotations

import logging

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.application.properties.contracts import (
    PropertyResult,
    ReplaceOwnershipCommand,
)
from baku.backend.application.properties.create_property import _to_result
from baku.backend.domain.owners.repositories import OwnerRepository
from baku.backend.domain.properties.entities import Ownership
from baku.backend.domain.properties.errors import (
    OwnerNotFoundForOwnership,
    PropertyNotFound,
    PropertyOwnershipRequired,
)
from baku.backend.domain.properties.policies import validate_ownership_inputs
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)

logger = logging.getLogger(__name__)


def replace_property_ownership(
    cmd: ReplaceOwnershipCommand,
    property_repo: PropertyRepository,
    ownership_repo: OwnershipRepository,
    owner_repo: OwnerRepository,
    uow: PropertyUnitOfWorkPort,
) -> PropertyResult:
    property_ = property_repo.find_by_id(cmd.property_id)
    if property_ is None:
        raise PropertyNotFound()

    if not cmd.ownerships:
        raise PropertyOwnershipRequired()

    # Validate percentage inputs
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

    now = utcnow()
    now_str = now.isoformat()

    # Update property audit fields to reflect this ownership change
    property_.updated_at = now
    property_.updated_by = cmd.updated_by
    property_repo.save(property_)

    # Soft-delete all current active ownerships for this property
    ownership_repo.soft_delete_active_by_property(
        property_id=cmd.property_id,
        deleted_by=cmd.updated_by,
        now=now_str,
    )

    # Create new ownerships
    new_ownerships = []
    for o in cmd.ownerships:
        ownership = Ownership.new(
            property_id=cmd.property_id,
            owner_id=o.owner_id,
            ownership_percentage=o.ownership_percentage,
            created_by=cmd.updated_by,
            now=now,
        )
        ownership_repo.save(ownership)
        new_ownerships.append(ownership)

    uow.commit()

    logger.info(
        "replace_property_ownership_completed",
        extra={
            "operation": "replace_property_ownership",
            "property_id": cmd.property_id,
        },
    )

    return _to_result(property_, new_ownerships)
