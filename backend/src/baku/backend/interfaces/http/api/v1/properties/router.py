"""Properties router — CRUD endpoints for F-0003.

Routes (versioned prefix /api/v1/properties, ADR-0004):
  POST   /                                    — create property with ownership (US1)
  GET    /                                    — list properties (US2)
  GET    /{property_id}                       — get property detail (US2)
  PATCH  /{property_id}                       — update property (US3)
  PUT    /{property_id}/ownership             — replace ownership set (US3)
  DELETE /{property_id}                       — soft-delete property + cascade (US4)
  GET    /{property_id}/owners                — list active owners of a property (US2)

Route (versioned prefix /api/v1/owners, ADR-0004 — cross-query):
  GET    /api/v1/owners/{owner_id}/properties — list properties for an owner (US2)

Authentication is mandatory on all endpoints (ADR-0005).
No PII in structured logs (ADR-0009).
Pagination defaults from centralised config (ADR-0013).
"""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from baku.backend.application.auth.token_validator import TokenClaims
from baku.backend.application.properties.contracts import (
    CreatePropertyCommand,
    DeletePropertyCommand,
    OwnershipInput,
    ReplaceOwnershipCommand,
    UpdatePropertyCommand,
)
from baku.backend.application.properties.create_property import create_property
from baku.backend.application.properties.delete_property import delete_property
from baku.backend.application.properties.query_properties import (
    get_property_detail,
    list_owner_properties,
    list_properties,
    list_property_owners,
)
from baku.backend.application.properties.update_ownership import (
    replace_property_ownership,
)
from baku.backend.application.properties.update_property import update_property
from baku.backend.domain.owners.repositories import OwnerRepository
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)
from baku.backend.infrastructure.config.runtime_settings import (
    RuntimeConfigurationProvider,
)
from baku.backend.interfaces.http.api.v1.properties.schemas import (
    CreatePropertyRequest,
    OwnershipListResponse,
    OwnershipResponse,
    PropertyListResponse,
    PropertyResponse,
    ReplaceOwnershipRequest,
    UpdatePropertyRequest,
)
from baku.backend.interfaces.http.dependencies.owner_deps import get_owner_repo
from baku.backend.interfaces.http.dependencies.property_deps import (
    get_ownership_repo,
    get_property_repo,
    get_property_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.require_auth import (
    get_current_claims,
)

router = APIRouter(prefix="/api/v1/properties", tags=["properties"])
# Cross-resource router: /api/v1/owners/{owner_id}/properties
owners_cross_router = APIRouter(prefix="/api/v1/owners", tags=["owners"])
CURRENT_CLAIMS_DEP = Depends(get_current_claims)
logger = logging.getLogger(__name__)


def _get_pagination_defaults() -> tuple[int, int]:
    """Return (default_page_size, max_page_size) from centralised config (ADR-0013)."""
    profile = RuntimeConfigurationProvider().get_profile()
    default_size = int(
        profile.values.get("pagination.default_page_size", "20")
    )
    max_size = int(profile.values.get("pagination.max_page_size", "100"))
    return default_size, max_size


def _cap_page_size(page_size: int) -> int:
    _, max_size = _get_pagination_defaults()
    return min(page_size, max_size)


def _result_to_response(result: object) -> PropertyResponse:
    return PropertyResponse.model_validate(result)


# ---------------------------------------------------------------------------
# US1: Create property
# ---------------------------------------------------------------------------


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PropertyResponse,
    response_model_exclude_none=True,
)
def post_create_property(
    body: CreatePropertyRequest,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    property_repo: Annotated[PropertyRepository, Depends(get_property_repo)],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
    owner_repo: Annotated[OwnerRepository, Depends(get_owner_repo)],
    uow: Annotated[PropertyUnitOfWorkPort, Depends(get_property_unit_of_work)],
) -> PropertyResponse:
    logger.info(
        "http_properties_create_started",
        extra={"method": "POST", "path": "/api/v1/properties"},
    )
    # (full path shown in log; relative route registered)
    cmd = CreatePropertyCommand(
        name=body.name,
        type=body.type,
        created_by=claims.sub,
        ownerships=[
            OwnershipInput(
                owner_id=o.owner_id,
                ownership_percentage=o.ownership_percentage,
            )
            for o in body.ownerships
        ],
        description=body.description,
        address=body.address,
        city=body.city,
        postal_code=body.postal_code,
        province=body.province,
        country=body.country,
        cadastral_reference=body.cadastral_reference,
        cadastral_value=body.cadastral_value,
        cadastral_land_value=body.cadastral_land_value,
        cadastral_value_revised=body.cadastral_value_revised,
        acquisition_date=body.acquisition_date,
        acquisition_type=body.acquisition_type,
        transfer_date=body.transfer_date,
        transfer_type=body.transfer_type,
        fiscal_nature=body.fiscal_nature,
        fiscal_situation=body.fiscal_situation,
    )
    result = create_property(
        cmd=cmd,
        property_repo=property_repo,
        ownership_repo=ownership_repo,
        owner_repo=owner_repo,
        uow=uow,
    )
    logger.info(
        "http_properties_create_completed",
        extra={
            "method": "POST",
            "path": "/api/v1/properties",
            "status_code": 201,
            "property_id": result.property_id,
        },
    )
    return _result_to_response(result)


# ---------------------------------------------------------------------------
# US2: Query properties
# ---------------------------------------------------------------------------


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PropertyListResponse,
    response_model_exclude_none=True,
)
def get_list_properties(
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    property_repo: Annotated[PropertyRepository, Depends(get_property_repo)],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    include_deleted: bool = Query(default=False),
) -> PropertyListResponse:
    capped = _cap_page_size(page_size)
    result = list_properties(
        property_repo=property_repo,
        ownership_repo=ownership_repo,
        page=page,
        page_size=capped,
        include_deleted=include_deleted,
    )
    return PropertyListResponse(
        items=[_result_to_response(p) for p in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


@router.get(
    "/{property_id}",
    status_code=status.HTTP_200_OK,
    response_model=PropertyResponse,
    response_model_exclude_none=True,
)
def get_property(
    property_id: str,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    property_repo: Annotated[PropertyRepository, Depends(get_property_repo)],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
    include_deleted: bool = Query(default=False),
) -> PropertyResponse:
    result = get_property_detail(
        property_id=property_id,
        property_repo=property_repo,
        ownership_repo=ownership_repo,
        include_deleted=include_deleted,
    )
    return _result_to_response(result)


@router.get(
    "/{property_id}/owners",
    status_code=status.HTTP_200_OK,
    response_model=OwnershipListResponse,
    response_model_exclude_none=True,
)
def get_property_owners(
    property_id: str,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    property_repo: Annotated[PropertyRepository, Depends(get_property_repo)],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
) -> OwnershipListResponse:
    ownerships = list_property_owners(
        property_id=property_id,
        property_repo=property_repo,
        ownership_repo=ownership_repo,
    )
    items = [OwnershipResponse.model_validate(o) for o in ownerships]
    return OwnershipListResponse(
        items=items,
        total=len(items),
        page=1,
        page_size=len(items),
    )


@owners_cross_router.get(
    "/{owner_id}/properties",
    status_code=status.HTTP_200_OK,
    response_model=PropertyListResponse,
    response_model_exclude_none=True,
)
def get_owner_properties(
    owner_id: str,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
) -> PropertyListResponse:
    capped = _cap_page_size(page_size)
    result = list_owner_properties(
        owner_id=owner_id,
        ownership_repo=ownership_repo,
        page=page,
        page_size=capped,
    )
    return PropertyListResponse(
        items=[_result_to_response(p) for p in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


# ---------------------------------------------------------------------------
# US3: Update property and ownership
# ---------------------------------------------------------------------------


@router.patch(
    "/{property_id}",
    status_code=status.HTTP_200_OK,
    response_model=PropertyResponse,
    response_model_exclude_none=True,
)
def patch_update_property(
    property_id: str,
    body: UpdatePropertyRequest,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    property_repo: Annotated[PropertyRepository, Depends(get_property_repo)],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
    uow: Annotated[PropertyUnitOfWorkPort, Depends(get_property_unit_of_work)],
) -> PropertyResponse:
    cmd = UpdatePropertyCommand(
        property_id=property_id,
        updated_by=claims.sub,
        name=body.name,
        type=body.type,
        description=body.description,
        address=body.address,
        city=body.city,
        postal_code=body.postal_code,
        province=body.province,
        country=body.country,
        cadastral_reference=body.cadastral_reference,
        cadastral_value=body.cadastral_value,
        cadastral_land_value=body.cadastral_land_value,
        cadastral_value_revised=body.cadastral_value_revised,
        acquisition_date=body.acquisition_date,
        acquisition_type=body.acquisition_type,
        transfer_date=body.transfer_date,
        transfer_type=body.transfer_type,
        fiscal_nature=body.fiscal_nature,
        fiscal_situation=body.fiscal_situation,
    )
    result = update_property(
        cmd=cmd,
        property_repo=property_repo,
        ownership_repo=ownership_repo,
        uow=uow,
    )
    return _result_to_response(result)


@router.put(
    "/{property_id}/ownership",
    status_code=status.HTTP_200_OK,
    response_model=PropertyResponse,
    response_model_exclude_none=True,
)
def put_replace_ownership(
    property_id: str,
    body: ReplaceOwnershipRequest,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    property_repo: Annotated[PropertyRepository, Depends(get_property_repo)],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
    owner_repo: Annotated[OwnerRepository, Depends(get_owner_repo)],
    uow: Annotated[PropertyUnitOfWorkPort, Depends(get_property_unit_of_work)],
) -> PropertyResponse:
    cmd = ReplaceOwnershipCommand(
        property_id=property_id,
        ownerships=[
            OwnershipInput(
                owner_id=o.owner_id,
                ownership_percentage=o.ownership_percentage,
            )
            for o in body.ownerships
        ],
        updated_by=claims.sub,
    )
    result = replace_property_ownership(
        cmd=cmd,
        property_repo=property_repo,
        ownership_repo=ownership_repo,
        owner_repo=owner_repo,
        uow=uow,
    )
    return _result_to_response(result)


# ---------------------------------------------------------------------------
# US4: Soft-delete property
# ---------------------------------------------------------------------------


@router.delete(
    "/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_property_endpoint(
    property_id: str,
    claims: Annotated[TokenClaims, CURRENT_CLAIMS_DEP],
    property_repo: Annotated[PropertyRepository, Depends(get_property_repo)],
    ownership_repo: Annotated[
        OwnershipRepository, Depends(get_ownership_repo)
    ],
    uow: Annotated[PropertyUnitOfWorkPort, Depends(get_property_unit_of_work)],
) -> Response:
    cmd = DeletePropertyCommand(property_id=property_id, deleted_by=claims.sub)
    delete_property(
        cmd=cmd,
        property_repo=property_repo,
        ownership_repo=ownership_repo,
        uow=uow,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
