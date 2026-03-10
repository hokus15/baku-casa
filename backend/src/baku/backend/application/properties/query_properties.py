"""Use cases: query properties and ownerships — F-0003 US2.

Raises:
    PropertyNotFound — property_id does not exist or is soft-deleted.
"""

from __future__ import annotations

import logging

from baku.backend.application.properties.contracts import (
    OwnershipResult,
    PropertyListResult,
    PropertyResult,
)
from baku.backend.application.properties.create_property import _to_result
from baku.backend.domain.properties.errors import PropertyNotFound
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
)

logger = logging.getLogger(__name__)

_DEFAULT_PAGE = 1
_DEFAULT_PAGE_SIZE = 20


def get_property_detail(
    property_id: str,
    property_repo: PropertyRepository,
    ownership_repo: OwnershipRepository,
    include_deleted: bool = False,
) -> PropertyResult:
    property_ = property_repo.find_by_id(
        property_id, include_deleted=include_deleted
    )
    if property_ is None:
        raise PropertyNotFound()
    ownerships = ownership_repo.list_active_by_property(property_id)
    return _to_result(property_, ownerships)


def list_properties(
    property_repo: PropertyRepository,
    ownership_repo: OwnershipRepository,
    page: int = _DEFAULT_PAGE,
    page_size: int = _DEFAULT_PAGE_SIZE,
    include_deleted: bool = False,
) -> PropertyListResult:
    logger.info(
        "list_properties_started",
        extra={
            "operation": "list_properties",
            "page": page,
            "page_size": page_size,
        },
    )
    result = property_repo.list(
        page=page, page_size=page_size, include_deleted=include_deleted
    )
    items = []
    for prop in result.items:
        ownerships = ownership_repo.list_active_by_property(prop.property_id)
        items.append(_to_result(prop, ownerships))
    return PropertyListResult(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


def list_property_owners(
    property_id: str,
    property_repo: PropertyRepository,
    ownership_repo: OwnershipRepository,
) -> list[OwnershipResult]:
    """Return all active ownerships for a given property."""
    property_ = property_repo.find_by_id(property_id)
    if property_ is None:
        raise PropertyNotFound()
    ownerships = ownership_repo.list_active_by_property(property_id)
    return [
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


def list_owner_properties(
    owner_id: str,
    ownership_repo: OwnershipRepository,
    page: int = _DEFAULT_PAGE,
    page_size: int = _DEFAULT_PAGE_SIZE,
) -> PropertyListResult:
    """Return all active properties for a given owner (cross-query)."""
    result = ownership_repo.list_active_by_owner(
        owner_id=owner_id, page=page, page_size=page_size
    )
    items = []
    for prop in result.items:
        ownerships = ownership_repo.list_active_by_property(prop.property_id)
        items.append(_to_result(prop, ownerships))
    return PropertyListResult(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )
