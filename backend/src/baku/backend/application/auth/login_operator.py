"""Use case: Login operator — validate credentials, apply throttle, issue JWT.

Raises:
  LockedTemporarily  — operator is in active lockout window.
  InvalidCredentials — username not found or password mismatch.
"""

from __future__ import annotations

from dataclasses import dataclass

from baku.backend.application.auth.auth_policy_port import AuthPolicyPort
from baku.backend.application.auth.password_hasher_port import PasswordHasherPort
from baku.backend.application.auth.token_issuer_port import TokenIssuerPort
from baku.backend.application.auth.token_validator import TokenClaims
from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import LoginThrottleState
from baku.backend.domain.auth.errors import InvalidCredentials, LockedTemporarily
from baku.backend.domain.auth.repositories import (
    OperatorRepository,
    ThrottleStateRepository,
    UnitOfWorkPort,
)


@dataclass
class LoginResult:
    access_token: str
    claims: TokenClaims


def login_operator(
    username: str,
    password: str,
    op_repo: OperatorRepository,
    throttle_repo: ThrottleStateRepository,
    policy: AuthPolicyPort,
    hasher: PasswordHasherPort,
    token_issuer: TokenIssuerPort,
    uow: UnitOfWorkPort,
) -> LoginResult:
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
    if operator is None or not hasher.verify(password, operator.password_hash):
        if operator is not None and throttle is not None:
            throttle.record_failure(
                now,
                policy.max_failed_attempts,
                policy.lockout_minutes,
            )
            throttle_repo.save(throttle)
            uow.commit()
        raise InvalidCredentials()

    # Successful login
    assert throttle is not None
    throttle.record_success()
    throttle_repo.save(throttle)

    operator.record_login(now)
    op_repo.save(operator)
    uow.commit()

    access_token, claims = token_issuer.issue(
        operator_id=operator.operator_id,
        credential_version=operator.credential_version,
        ttl_seconds=policy.token_ttl_seconds,
    )
    return LoginResult(access_token=access_token, claims=claims)
