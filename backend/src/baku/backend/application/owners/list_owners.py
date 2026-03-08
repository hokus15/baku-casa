"""Use case: ListOwners — paginated list with optional filters.

page_size is capped at 100 by the repository layer.
"""

from __future__ import annotations

import logging

from baku.backend.domain.owners.repositories import OwnerPage, OwnerRepository
from baku.backend.domain.owners.tax_id_normalizer import normalize_tax_id

logger = logging.getLogger(__name__)

_DEFAULT_PAGE = 1
_DEFAULT_PAGE_SIZE = 20


def list_owners(
    owner_repo: OwnerRepository,
    page: int = _DEFAULT_PAGE,
    page_size: int = _DEFAULT_PAGE_SIZE,
    tax_id: str | None = None,
    legal_name: str | None = None,
    include_deleted: bool = False,
) -> OwnerPage:
    logger.info(
        "list_owners_started",
        extra={"operation": "list_owners", "page": page, "page_size": page_size},
    )
    # Normalize tax_id filter so search is consistent with creation uniqueness
    normalized_tax_id = normalize_tax_id(tax_id) if tax_id else None

    return owner_repo.list(
        page=page,
        page_size=page_size,
        tax_id=normalized_tax_id,
        legal_name=legal_name,
        include_deleted=include_deleted,
    )
