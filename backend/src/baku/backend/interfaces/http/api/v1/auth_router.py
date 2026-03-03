"""Auth router — all authentication endpoints for F-0001.

Routes (versioned prefix /api/v1/auth, ADR-0004):
  POST /bootstrap   — bootstrap initial operator (US1)
  POST /login       — authenticate and issue JWT (US2)
  POST /logout      — revoke current token (US2)
  PUT  /password    — rotate password, global token revocation (US3)
"""

from __future__ import annotations

from collections.abc import Generator

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from baku.backend.application.auth.bootstrap_operator import bootstrap_operator
from baku.backend.application.auth.change_operator_password import (
    change_operator_password,
)
from baku.backend.application.auth.login_operator import login_operator
from baku.backend.application.auth.logout_operator import logout_operator
from baku.backend.infrastructure.persistence.sqlite.db import get_session_factory
from baku.backend.infrastructure.security.jwt_service import TokenClaims
from baku.backend.interfaces.http.api.v1.schemas.auth_bootstrap import BootstrapRequest
from baku.backend.interfaces.http.api.v1.schemas.auth_login import (
    LoginRequest,
    LoginResponse,
)
from baku.backend.interfaces.http.api.v1.schemas.auth_password import PasswordChangeRequest
from baku.backend.interfaces.http.dependencies.require_auth import get_current_claims

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
CURRENT_CLAIMS_DEP = Depends(get_current_claims)


def _get_session() -> Generator[Session, None, None]:
    factory = get_session_factory()
    with factory() as session:
        yield session


@router.post("/bootstrap", status_code=status.HTTP_201_CREATED)
def post_bootstrap(body: BootstrapRequest) -> Response:
    """Bootstrap operator credentials on first run (FR-001, FR-002)."""
    factory = get_session_factory()
    with factory() as session:
        bootstrap_operator(body.username, body.password, session)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def post_login(body: LoginRequest) -> LoginResponse:
    """Authenticate operator and issue access token (FR-003, FR-016–FR-020)."""
    factory = get_session_factory()
    with factory() as session:
        result = login_operator(body.username, body.password, session)
    return LoginResponse(
        access_token=result.access_token,
        token_type="Bearer",
        expires_at=result.claims.exp.isoformat(),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def post_logout(
    claims: TokenClaims = CURRENT_CLAIMS_DEP,
) -> Response:
    """Revoke current token explicitly (FR-006)."""
    factory = get_session_factory()
    with factory() as session:
        logout_operator(claims, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def put_password(
    body: PasswordChangeRequest,
    claims: TokenClaims = CURRENT_CLAIMS_DEP,
) -> Response:
    """Rotate operator password, revoke prior tokens globally (FR-007, FR-008)."""
    factory = get_session_factory()
    with factory() as session:
        change_operator_password(
            operator_id=claims.sub,
            current_password=body.current_password,
            new_password=body.new_password,
            session=session,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
