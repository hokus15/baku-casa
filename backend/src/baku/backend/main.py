"""FastAPI application entry point — backend root.

Composition root: this is the only module that imports from both the
Interfaces and Infrastructure layers simultaneously in order to wire
concrete implementations into the dependency graph (ADR-0002).

Startup sequence (ADR-0013 fail-fast):
  1. Centralized configuration is loaded and validated before any router
     is mounted.  If required keys are missing the process aborts with a
     full aggregated error report — no partial startup.
  2. Auth settings are derived from the validated centralized profile.
  3. Routers are included only after configuration is confirmed valid.

Dependency direction enforced via app.dependency_overrides:
  Interfaces layer stubs → Infrastructure concrete implementations
  All other modules must import only from Application or Domain.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import cast

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from baku.backend.application.auth.auth_policy_port import AuthPolicyPort
from baku.backend.application.auth.password_hasher_port import PasswordHasherPort
from baku.backend.application.auth.token_issuer_port import TokenIssuerPort
from baku.backend.domain.auth.repositories import (
    OperatorRepository,
    RevokedTokenRepository,
    ThrottleStateRepository,
    UnitOfWorkPort,
)
from baku.backend.infrastructure.config.auth_policy_provider import AuthSettingsPolicy
from baku.backend.infrastructure.config.auth_settings import get_auth_settings
from baku.backend.infrastructure.config.runtime_settings import RuntimeConfigurationProvider
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteOperatorRepository,
    SqliteRevokedTokenRepository,
    SqliteThrottleStateRepository,
    SqliteUnitOfWork,
)
from baku.backend.infrastructure.persistence.sqlite.db import get_session_factory
from baku.backend.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from baku.backend.infrastructure.security.jwt_token_issuer import JwtTokenIssuer
from baku.backend.infrastructure.security.jwt_token_validator import get_jwt_token_validator
from baku.backend.interfaces.http.api.v1.auth_router import router as auth_router
from baku.backend.interfaces.http.dependencies.db_session import get_session
from baku.backend.interfaces.http.dependencies.repo_deps import (
    get_operator_repo,
    get_revoked_token_repo,
    get_throttle_repo,
    get_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.require_auth import get_token_validator
from baku.backend.interfaces.http.dependencies.service_deps import (
    get_auth_policy,
    get_password_hasher,
    get_token_issuer,
)
from baku.backend.interfaces.http.error_mapper import register_error_handlers
from baku.backend.interfaces.http.middleware.correlation_id import CorrelationIdMiddleware

# ── Centralized configuration bootstrap (ADR-0013, fail-fast) ────────────────
# Validate configuration before any other component is initialised.
# AggregatedConfigurationError is raised here if required keys are absent;
# FastAPI will never reach router inclusion in that case.
_config_provider = RuntimeConfigurationProvider()
_config_provider.get_profile()  # triggers validation; aborts process on error


app = FastAPI(
    title="Baku Casa Backend",
    version="1.0.0",
    description="Baku Casa property management backend — MVP1",
)

# ── Concrete dependency implementations (infrastructure) ──────────────────────


def _sqlite_session() -> Generator[Session, None, None]:
    """Yield a single SQLAlchemy session per request; auto-closed afterward."""
    factory = get_session_factory()
    with factory() as session:
        yield session


def _operator_repo(session: object = Depends(get_session)) -> OperatorRepository:
    return SqliteOperatorRepository(cast(Session, session))


def _revoked_token_repo(session: object = Depends(get_session)) -> RevokedTokenRepository:
    return SqliteRevokedTokenRepository(cast(Session, session))


def _throttle_repo(session: object = Depends(get_session)) -> ThrottleStateRepository:
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


# ── Dependency wiring (composition root) ──────────────────────────────────────
# Override every abstract stub in the Interfaces layer with a concrete
# Infrastructure implementation.  The Interfaces layer never imports
# Infrastructure directly — all coupling flows through this mapping.
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
    }
)

# ── Middleware (registered before routes) ─────────────────────────────────
app.add_middleware(CorrelationIdMiddleware)

# ── Error handlers ──────────────────────────────────────────────────────
register_error_handlers(app)

# ── Routers ────────────────────────────────────────────────────────────
app.include_router(auth_router)
