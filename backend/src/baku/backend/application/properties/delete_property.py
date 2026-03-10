"""Use case: DeleteProperty — soft-delete a property with cascade — F-0003 US4.

Soft-deletes the property and cascades soft-delete to all active ownerships.

Raises:
    PropertyNotFound — property_id does not exist or already soft-deleted.
"""

from __future__ import annotations

import logging

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.application.properties.contracts import DeletePropertyCommand
from baku.backend.domain.properties.errors import PropertyNotFound
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)

logger = logging.getLogger(__name__)


def delete_property(
    cmd: DeletePropertyCommand,
    property_repo: PropertyRepository,
    ownership_repo: OwnershipRepository,
    uow: PropertyUnitOfWorkPort,
) -> None:
    property_ = property_repo.find_by_id(cmd.property_id)
    if property_ is None:
        raise PropertyNotFound()

    now = utcnow()
    now_str = now.isoformat()

    # Cascade: soft-delete all active ownerships first
    ownership_repo.soft_delete_active_by_property(
        property_id=cmd.property_id,
        deleted_by=cmd.deleted_by,
        now=now_str,
    )

    # Soft-delete the property
    property_.deleted_at = now
    property_.deleted_by = cmd.deleted_by
    property_repo.save(property_)

    uow.commit()

    logger.info(
        "delete_property_completed",
        extra={"operation": "delete_property", "property_id": cmd.property_id},
    )
