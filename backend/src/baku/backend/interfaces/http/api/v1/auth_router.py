"""Auth router — all authentication endpoints for F-0001.

Routes (versioned prefix /api/v1/auth, ADR-0004):
  POST /bootstrap   — bootstrap initial operator (US1)
  POST /login       — authenticate and issue JWT (US2)
  POST /logout      — revoke current token (US2)
  PUT  /password    — rotate password, global token revocation (US3)

This module imports only from Application, Domain, and Interfaces layers.
All Infrastructure is injected by the composition root (main.py) via
app.dependency_overrides (ADR-0002).
"""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from baku.backend.application.auth.auth_policy_port import AuthPolicyPort
from baku.backend.application.auth.bootstrap_operator import bootstrap_operator
from baku.backend.application.auth.change_operator_password import change_operator_password
from baku.backend.application.auth.login_operator import login_operator
from baku.backend.application.auth.logout_operator import logout_operator
from baku.backend.application.auth.password_hasher_port import PasswordHasherPort
from baku.backend.application.auth.token_issuer_port import TokenIssuerPort
from baku.backend.application.auth.token_validator import TokenClaims
from baku.backend.domain.auth.repositories import (
    OperatorRepository,
    RevokedTokenRepository,
    ThrottleStateRepository,
    UnitOfWorkPort,
)
from baku.backend.interfaces.http.api.v1.schemas.auth_bootstrap import BootstrapRequest
from baku.backend.interfaces.http.api.v1.schemas.auth_login import LoginRequest, LoginResponse
from baku.backend.interfaces.http.api.v1.schemas.auth_password import PasswordChangeRequest
from baku.backend.interfaces.http.dependencies.repo_deps import (
    get_operator_repo,
    get_revoked_token_repo,
    get_throttle_repo,
    get_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.require_auth import get_current_claims
from baku.backend.interfaces.http.dependencies.service_deps import (
    get_auth_policy,
    get_password_hasher,
    get_token_issuer,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
CURRENT_CLAIMS_DEP = Depends(get_current_claims)
logger = logging.getLogger(__name__)


@router.post("/bootstrap", status_code=status.HTTP_201_CREATED)
def post_bootstrap(
    body: BootstrapRequest,
    op_repo: Annotated[OperatorRepository, Depends(get_operator_repo)],
    hasher: Annotated[PasswordHasherPort, Depends(get_password_hasher)],
    uow: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> Response:
    """Bootstrap operator credentials on first run (FR-001, FR-002)."""
    logger.info(
        "http_auth_bootstrap_started",
        extra={"method": "POST", "path": "/api/v1/auth/bootstrap"},
    )
    bootstrap_operator(body.username, body.password, op_repo, hasher, uow)
    logger.info(
        "http_auth_bootstrap_completed",
        extra={"method": "POST", "path": "/api/v1/auth/bootstrap", "status_code": 201},
    )
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def post_login(
    body: LoginRequest,
    op_repo: Annotated[OperatorRepository, Depends(get_operator_repo)],
    throttle_repo: Annotated[ThrottleStateRepository, Depends(get_throttle_repo)],
    policy: Annotated[AuthPolicyPort, Depends(get_auth_policy)],
    hasher: Annotated[PasswordHasherPort, Depends(get_password_hasher)],
    token_issuer: Annotated[TokenIssuerPort, Depends(get_token_issuer)],
    uow: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> LoginResponse:
    """Authenticate operator and issue access token (FR-003, FR-016–FR-020)."""
    logger.info(
        "http_auth_login_started",
        extra={"method": "POST", "path": "/api/v1/auth/login"},
    )
    result = login_operator(
        body.username,
        body.password,
        op_repo,
        throttle_repo,
        policy,
        hasher,
        token_issuer,
        uow,
    )
    logger.info(
        "http_auth_login_completed",
        extra={"method": "POST", "path": "/api/v1/auth/login", "status_code": 200},
    )
    return LoginResponse(
        access_token=result.access_token,
        token_type="Bearer",
        expires_at=result.claims.exp.isoformat(),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def post_logout(
    claims: TokenClaims = CURRENT_CLAIMS_DEP,
    revoked_repo: Annotated[RevokedTokenRepository, Depends(get_revoked_token_repo)] = ...,  # type: ignore[assignment]
    uow: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)] = ...,  # type: ignore[assignment]
) -> Response:
    """Revoke current token explicitly (FR-006)."""
    logger.info(
        "http_auth_logout_started",
        extra={"method": "POST", "path": "/api/v1/auth/logout"},
    )
    logout_operator(claims, revoked_repo, uow)
    logger.info(
        "http_auth_logout_completed",
        extra={"method": "POST", "path": "/api/v1/auth/logout", "status_code": 204},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def put_password(
    body: PasswordChangeRequest,
    claims: TokenClaims = CURRENT_CLAIMS_DEP,
    op_repo: Annotated[OperatorRepository, Depends(get_operator_repo)] = ...,  # type: ignore[assignment]
    hasher: Annotated[PasswordHasherPort, Depends(get_password_hasher)] = ...,  # type: ignore[assignment]
    uow: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)] = ...,  # type: ignore[assignment]
) -> Response:
    """Rotate operator password, revoke prior tokens globally (FR-007, FR-008)."""
    logger.info(
        "http_auth_password_started",
        extra={"method": "PUT", "path": "/api/v1/auth/password"},
    )
    change_operator_password(
        operator_id=claims.sub,
        current_password=body.current_password,
        new_password=body.new_password,
        op_repo=op_repo,
        hasher=hasher,
        uow=uow,
    )
    logger.info(
        "http_auth_password_completed",
        extra={"method": "PUT", "path": "/api/v1/auth/password", "status_code": 204},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
