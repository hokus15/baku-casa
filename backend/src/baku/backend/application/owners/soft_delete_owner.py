"""Use case: SoftDeleteOwner — mark an active owner as deleted (auditable soft delete).

Raises:
  OwnerNotFound      — owner does not exist or is already deleted.
"""

from __future__ import annotations

import logging

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.owners.errors import OwnerNotFound
from baku.backend.domain.owners.repositories import OwnerRepository, OwnerUnitOfWorkPort

logger = logging.getLogger(__name__)


def soft_delete_owner(
    owner_id: str,
    deleted_by: str,
    owner_repo: OwnerRepository,
    uow: OwnerUnitOfWorkPort,
) -> None:
    logger.info(
        "soft_delete_owner_started",
        extra={"operation": "soft_delete_owner", "owner_id": owner_id},
    )
    owner = owner_repo.find_by_id(owner_id, include_deleted=False)
    if owner is None:
        raise OwnerNotFound()

    now = utcnow()
    owner.deleted_at = now
    owner.deleted_by = deleted_by
    owner.updated_at = now
    owner.updated_by = deleted_by

    owner_repo.save(owner)
    uow.commit()

    logger.info(
        "soft_delete_owner_completed",
        extra={"operation": "soft_delete_owner", "owner_id": owner_id},
    )
