"""Owners router — CRUD endpoints for F-0002.

Routes (versioned prefix /api/v1/owners, ADR-0004):
  POST   /              — create owner (US1)
  GET    /              — list/search owners (US3)
  GET    /{owner_id}    — get owner detail (US2)
  PATCH  /{owner_id}    — update owner (US4)
  DELETE /{owner_id}    — soft delete owner (US5)

Authentication is mandatory on all endpoints (ADR-0005).
No PII in structured logs (research.md §5, ADR-0009).
"""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from baku.backend.application.auth.token_validator import TokenClaims
from baku.backend.application.owners.create_owner import create_owner
from baku.backend.application.owners.get_owner_by_id import get_owner_by_id
from baku.backend.application.owners.list_owners import list_owners
from baku.backend.application.owners.soft_delete_owner import soft_delete_owner
from baku.backend.application.owners.update_owner import OwnerUpdate, update_owner
from baku.backend.domain.owners.repositories import OwnerRepository, OwnerUnitOfWorkPort
from baku.backend.interfaces.http.api.v1.owners.schemas import (
    OwnerCreateRequest,
    OwnerListResponse,
    OwnerResponse,
    OwnerUpdateRequest,
)
from baku.backend.interfaces.http.dependencies.owner_deps import get_owner_repo, get_owner_unit_of_work
from baku.backend.interfaces.http.dependencies.require_auth import get_current_claims

router = APIRouter(prefix="/api/v1/owners", tags=["owners"])
CURRENT_CLAIMS_DEP = Depends(get_current_claims)
logger = logging.getLogger(__name__)


def _owner_to_response(owner: object) -> OwnerResponse:
    return OwnerResponse.model_validate(owner)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OwnerResponse, response_model_exclude_none=True)
def post_create_owner(
    body: OwnerCreateRequest,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    owner_repo: Annotated[OwnerRepository, Depends(get_owner_repo)],
    uow: Annotated[OwnerUnitOfWorkPort, Depends(get_owner_unit_of_work)],
) -> OwnerResponse:
    """Create a new owner (US1). Requires authentication."""
    logger.info(
        "http_owners_create_started",
        extra={"method": "POST", "path": "/api/v1/owners"},
    )
    owner = create_owner(
        entity_type=body.entity_type,
        first_name=body.first_name,
        last_name=body.last_name,
        legal_name=body.legal_name,
        raw_tax_id=body.tax_id,
        fiscal_address_line1=body.fiscal_address_line1,
        fiscal_address_city=body.fiscal_address_city,
        fiscal_address_postal_code=body.fiscal_address_postal_code,
        fiscal_address_country=body.fiscal_address_country,
        created_by=claims.sub,
        owner_repo=owner_repo,
        uow=uow,
        email=body.email,
        land_line=body.land_line,
        land_line_country_code=body.land_line_country_code,
        mobile=body.mobile,
        mobile_country_code=body.mobile_country_code,
        stamp_image=body.stamp_image,
    )
    logger.info(
        "http_owners_create_completed",
        extra={"method": "POST", "path": "/api/v1/owners", "status_code": 201, "owner_id": owner.owner_id},
    )
    return _owner_to_response(owner)


@router.get("", status_code=status.HTTP_200_OK, response_model=OwnerListResponse, response_model_exclude_none=True)
def get_list_owners(
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    owner_repo: Annotated[OwnerRepository, Depends(get_owner_repo)],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    tax_id: str | None = Query(default=None),
    legal_name: str | None = Query(default=None),
    include_deleted: bool = Query(default=False),
) -> OwnerListResponse:
    """List and search owners with pagination (US3). Requires authentication."""
    logger.info(
        "http_owners_list_started",
        extra={"method": "GET", "path": "/api/v1/owners", "page": page, "page_size": page_size},
    )
    result = list_owners(
        owner_repo=owner_repo,
        page=page,
        page_size=page_size,
        tax_id=tax_id,
        legal_name=legal_name,
        include_deleted=include_deleted,
    )
    logger.info(
        "http_owners_list_completed",
        extra={"method": "GET", "path": "/api/v1/owners", "status_code": 200, "total": result.total},
    )
    return OwnerListResponse(
        items=[_owner_to_response(o) for o in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


@router.get(
    "/{owner_id}", status_code=status.HTTP_200_OK, response_model=OwnerResponse, response_model_exclude_none=True
)
def get_owner_detail(
    owner_id: str,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    owner_repo: Annotated[OwnerRepository, Depends(get_owner_repo)],
    include_deleted: bool = Query(default=False),
) -> OwnerResponse:
    """Get owner detail by owner_id (US2). Requires authentication."""
    logger.info(
        "http_owners_detail_started",
        extra={"method": "GET", "path": "/api/v1/owners/{owner_id}", "owner_id": owner_id},
    )
    owner = get_owner_by_id(owner_id=owner_id, owner_repo=owner_repo, include_deleted=include_deleted)
    logger.info(
        "http_owners_detail_completed",
        extra={"method": "GET", "path": "/api/v1/owners/{owner_id}", "status_code": 200, "owner_id": owner_id},
    )
    return _owner_to_response(owner)


@router.patch(
    "/{owner_id}", status_code=status.HTTP_200_OK, response_model=OwnerResponse, response_model_exclude_none=True
)
def patch_update_owner(
    owner_id: str,
    body: OwnerUpdateRequest,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    owner_repo: Annotated[OwnerRepository, Depends(get_owner_repo)],
    uow: Annotated[OwnerUnitOfWorkPort, Depends(get_owner_unit_of_work)],
) -> OwnerResponse:
    """Update an active owner (US4). Requires authentication."""
    logger.info(
        "http_owners_update_started",
        extra={"method": "PATCH", "path": "/api/v1/owners/{owner_id}", "owner_id": owner_id},
    )
    patch = OwnerUpdate.from_provided(
        body.model_fields_set,
        entity_type=body.entity_type,
        first_name=body.first_name,
        last_name=body.last_name,
        legal_name=body.legal_name,
        tax_id=body.tax_id,
        fiscal_address_line1=body.fiscal_address_line1,
        fiscal_address_city=body.fiscal_address_city,
        fiscal_address_postal_code=body.fiscal_address_postal_code,
        fiscal_address_country=body.fiscal_address_country,
        email=body.email,
        land_line=body.land_line,
        land_line_country_code=body.land_line_country_code,
        mobile=body.mobile,
        mobile_country_code=body.mobile_country_code,
        stamp_image=body.stamp_image,
    )
    owner = update_owner(
        owner_id=owner_id,
        updated_by=claims.sub,
        patch=patch,
        owner_repo=owner_repo,
        uow=uow,
    )
    logger.info(
        "http_owners_update_completed",
        extra={"method": "PATCH", "path": "/api/v1/owners/{owner_id}", "status_code": 200, "owner_id": owner_id},
    )
    return _owner_to_response(owner)


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_soft_delete_owner(
    owner_id: str,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    owner_repo: Annotated[OwnerRepository, Depends(get_owner_repo)],
    uow: Annotated[OwnerUnitOfWorkPort, Depends(get_owner_unit_of_work)],
) -> Response:
    """Soft delete an owner (US5). Requires authentication."""
    logger.info(
        "http_owners_delete_started",
        extra={"method": "DELETE", "path": "/api/v1/owners/{owner_id}", "owner_id": owner_id},
    )
    soft_delete_owner(owner_id=owner_id, deleted_by=claims.sub, owner_repo=owner_repo, uow=uow)
    logger.info(
        "http_owners_delete_completed",
        extra={"method": "DELETE", "path": "/api/v1/owners/{owner_id}", "status_code": 204, "owner_id": owner_id},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
