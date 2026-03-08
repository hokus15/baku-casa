"""Use case: GetOwnerById — retrieve a single owner by owner_id.

Raises:
  OwnerNotFound — owner does not exist or is soft-deleted when include_deleted=False.
"""

from __future__ import annotations

import logging

from baku.backend.domain.owners.entities import Owner
from baku.backend.domain.owners.errors import OwnerNotFound
from baku.backend.domain.owners.repositories import OwnerRepository

logger = logging.getLogger(__name__)


def get_owner_by_id(
    owner_id: str,
    owner_repo: OwnerRepository,
    include_deleted: bool = False,
) -> Owner:
    logger.info(
        "get_owner_by_id_started",
        extra={"operation": "get_owner_by_id", "owner_id": owner_id},
    )
    owner = owner_repo.find_by_id(owner_id, include_deleted=include_deleted)
    if owner is None:
        raise OwnerNotFound()
    return owner
