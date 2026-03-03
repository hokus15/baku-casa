"""Use case: Login operator — validate credentials, apply throttle, issue JWT.

Raises:
  LockedTemporarily  — operator is in active lockout window.
  InvalidCredentials — username not found or password mismatch.
"""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import LoginThrottleState
from baku.backend.domain.auth.errors import InvalidCredentials, LockedTemporarily
from baku.backend.infrastructure.config.auth_settings import get_auth_settings
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteOperatorRepository,
    SqliteThrottleStateRepository,
)
from baku.backend.infrastructure.security.jwt_service import TokenClaims, issue_token
from baku.backend.infrastructure.security.password_hasher import verify_password


@dataclass
class LoginResult:
    access_token: str
    claims: TokenClaims


def login_operator(username: str, password: str, session: Session) -> LoginResult:
    settings = get_auth_settings()
    op_repo = SqliteOperatorRepository(session)
    throttle_repo = SqliteThrottleStateRepository(session)
    now = utcnow()

    operator = op_repo.find_by_username(username)

    # Load or initialise throttle state
    throttle: LoginThrottleState | None = None
    if operator is not None:
        throttle = throttle_repo.find_by_operator(operator.operator_id)
        if throttle is None:
            throttle = LoginThrottleState(operator_id=operator.operator_id)

        if throttle.is_blocked(now):
            raise LockedTemporarily()

    # Validate credentials
    if operator is None or not verify_password(password, operator.password_hash):
        if operator is not None and throttle is not None:
            throttle.record_failure(
                now,
                settings.max_failed_attempts,
                settings.lockout_minutes,
            )
            throttle_repo.save(throttle)
            session.commit()
        raise InvalidCredentials()

    # Successful login
    assert throttle is not None
    throttle.record_success()
    throttle_repo.save(throttle)

    operator.record_login(now)
    op_repo.save(operator)
    session.commit()

    token, claims = issue_token(
        operator_id=operator.operator_id,
        credential_version=operator.credential_version,
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        ttl_seconds=settings.token_ttl_seconds,
    )
    return LoginResult(access_token=token, claims=claims)
