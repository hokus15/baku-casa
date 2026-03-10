"""Dependency wiring — composition root for Infrastructure → Interfaces mapping (ADR-0002).

This is the single module in the Interfaces package that may import from both the
Interfaces layer and the Infrastructure layer simultaneously. Other Interfaces
modules may depend on Application and Domain code (plus external libraries and
other `baku.backend.interfaces.*` modules), but must not import from
`baku.backend.infrastructure.*` directly.

Within the Interfaces layer, all coupling to Infrastructure flows through this
mapping (ADR-0002 composition root discipline).

Responsibility: DEPENDENCY_COMPOSITION_WIRING (BootstrapInventory)
"""

from __future__ import annotations

from collections.abc import Generator
from typing import cast

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from baku.backend.application.auth.auth_policy_port import AuthPolicyPort
from baku.backend.application.auth.password_hasher_port import (
    PasswordHasherPort,
)
from baku.backend.application.auth.token_issuer_port import TokenIssuerPort
from baku.backend.domain.auth.repositories import (
    OperatorRepository,
    RevokedTokenRepository,
    ThrottleStateRepository,
    UnitOfWorkPort,
)
from baku.backend.domain.owners.repositories import (
    OwnerRepository,
    OwnerUnitOfWorkPort,
)
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)
from baku.backend.infrastructure.config.auth_policy_provider import (
    AuthSettingsPolicy,
)
from baku.backend.infrastructure.config.auth_settings import get_auth_settings
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteOperatorRepository,
    SqliteRevokedTokenRepository,
    SqliteThrottleStateRepository,
    SqliteUnitOfWork,
)
from baku.backend.infrastructure.persistence.sqlite.db import (
    get_session_factory,
)
from baku.backend.infrastructure.persistence.sqlite.owners.repositories import (
    SqliteOwnerRepository,
    SqliteOwnerUnitOfWork,
)
from baku.backend.infrastructure.persistence.sqlite.properties.repositories import (
    SqliteOwnershipRepository,
    SqlitePropertyRepository,
    SqlitePropertyUnitOfWork,
)
from baku.backend.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from baku.backend.infrastructure.security.jwt_token_issuer import (
    JwtTokenIssuer,
)
from baku.backend.infrastructure.security.jwt_token_validator import (
    get_jwt_token_validator,
)
from baku.backend.interfaces.http.dependencies.db_session import get_session
from baku.backend.interfaces.http.dependencies.owner_deps import (
    get_owner_repo,
    get_owner_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.property_deps import (
    get_ownership_repo,
    get_property_repo,
    get_property_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.repo_deps import (
    get_operator_repo,
    get_revoked_token_repo,
    get_throttle_repo,
    get_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.require_auth import (
    get_token_validator,
)
from baku.backend.interfaces.http.dependencies.service_deps import (
    get_auth_policy,
    get_password_hasher,
    get_token_issuer,
)


def _sqlite_session() -> Generator[Session, None, None]:
    """Yield a single SQLAlchemy session per request; auto-closed afterward."""
    factory = get_session_factory()
    with factory() as session:
        yield session


def _operator_repo(
    session: object = Depends(get_session),
) -> OperatorRepository:
    return SqliteOperatorRepository(cast(Session, session))


def _revoked_token_repo(
    session: object = Depends(get_session),
) -> RevokedTokenRepository:
    return SqliteRevokedTokenRepository(cast(Session, session))


def _throttle_repo(
    session: object = Depends(get_session),
) -> ThrottleStateRepository:
    return SqliteThrottleStateRepository(cast(Session, session))


def _unit_of_work(session: object = Depends(get_session)) -> UnitOfWorkPort:
    return SqliteUnitOfWork(cast(Session, session))


def _password_hasher() -> PasswordHasherPort:
    return BcryptPasswordHasher()


def _token_issuer() -> TokenIssuerPort:
    settings = get_auth_settings()
    return JwtTokenIssuer(settings.jwt_secret, settings.jwt_algorithm)


def _auth_policy() -> AuthPolicyPort:
    return AuthSettingsPolicy()


def _owner_repo(session: object = Depends(get_session)) -> OwnerRepository:
    return SqliteOwnerRepository(cast(Session, session))


def _owner_unit_of_work(
    session: object = Depends(get_session),
) -> OwnerUnitOfWorkPort:
    return SqliteOwnerUnitOfWork(cast(Session, session))


def _property_repo(
    session: object = Depends(get_session),
) -> PropertyRepository:
    return SqlitePropertyRepository(cast(Session, session))


def _ownership_repo(
    session: object = Depends(get_session),
) -> OwnershipRepository:
    return SqliteOwnershipRepository(cast(Session, session))


def _property_unit_of_work(
    session: object = Depends(get_session),
) -> PropertyUnitOfWorkPort:
    return SqlitePropertyUnitOfWork(cast(Session, session))


def wire_dependencies(app: FastAPI) -> None:
    """Override every abstract stub in the Interfaces layer with a concrete
    Infrastructure implementation.

    The Interfaces layer never imports Infrastructure directly — all coupling
    flows through this mapping (ADR-0002).
    """
    app.dependency_overrides.update(
        {
            get_session: _sqlite_session,
            get_operator_repo: _operator_repo,
            get_revoked_token_repo: _revoked_token_repo,
            get_throttle_repo: _throttle_repo,
            get_unit_of_work: _unit_of_work,
            get_password_hasher: _password_hasher,
            get_token_issuer: _token_issuer,
            get_auth_policy: _auth_policy,
            get_token_validator: get_jwt_token_validator,
            get_owner_repo: _owner_repo,
            get_owner_unit_of_work: _owner_unit_of_work,
            get_property_repo: _property_repo,
            get_ownership_repo: _ownership_repo,
            get_property_unit_of_work: _property_unit_of_work,
        }
    )
