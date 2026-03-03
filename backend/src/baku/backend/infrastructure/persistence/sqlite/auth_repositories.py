"""SQLite transactional repositories for authentication — infrastructure layer.

Maps between domain entities and ORM models.  All state-changing operations
are transactional (ADR-0003).
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from baku.backend.domain.auth.entities import (
    LoginThrottleState,
    Operator,
    RevocationReason,
    RevokedToken,
)
from baku.backend.domain.auth.errors import BootstrapAlreadyCompleted
from baku.backend.domain.auth.repositories import (
    OperatorRepository,
    RevokedTokenRepository,
    ThrottleStateRepository,
    UnitOfWorkPort,
)
from baku.backend.infrastructure.persistence.sqlite.orm_models import (
    LoginThrottleStateORM,
    OperatorORM,
    RevokedTokenORM,
)

_DT_FMT = "%Y-%m-%dT%H:%M:%S.%f+00:00"


def _dt_to_str(dt: datetime) -> str:
    return dt.isoformat()


def _str_to_dt(s: str) -> datetime:
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        dt = datetime.strptime(s, _DT_FMT)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _orm_to_operator(row: OperatorORM) -> Operator:
    return Operator(
        operator_id=row.operator_id,
        username=row.username,
        password_hash=row.password_hash,
        credential_version=row.credential_version,
        created_at=_str_to_dt(row.created_at),
        updated_at=_str_to_dt(row.updated_at) if row.updated_at else None,
        last_login_at=_str_to_dt(row.last_login_at) if row.last_login_at else None,
        is_active=row.is_active,
    )


def _orm_to_revoked_token(row: RevokedTokenORM) -> RevokedToken:
    return RevokedToken(
        token_jti=row.token_jti,
        operator_id=row.operator_id,
        revoked_at=_str_to_dt(row.revoked_at),
        expires_at=_str_to_dt(row.expires_at),
        reason=RevocationReason(row.reason),
    )


def _orm_to_throttle_state(row: LoginThrottleStateORM) -> LoginThrottleState:
    return LoginThrottleState(
        operator_id=row.operator_id,
        failed_attempts=row.failed_attempts,
        blocked_until=_str_to_dt(row.blocked_until) if row.blocked_until else None,
        last_failed_at=_str_to_dt(row.last_failed_at) if row.last_failed_at else None,
    )


class SqliteOperatorRepository(OperatorRepository):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_active(self) -> Operator | None:
        row = self._session.query(OperatorORM).filter(OperatorORM.is_active.is_(True)).first()
        return _orm_to_operator(row) if row else None

    def find_by_username(self, username: str) -> Operator | None:
        row = self._session.query(OperatorORM).filter(OperatorORM.username == username).first()
        return _orm_to_operator(row) if row else None

    def save(self, operator: Operator) -> None:
        row = self._session.get(OperatorORM, operator.operator_id)
        is_new = row is None
        if row is None:
            row = OperatorORM(operator_id=operator.operator_id)
            self._session.add(row)
        row.username = operator.username
        row.password_hash = operator.password_hash
        row.credential_version = operator.credential_version
        row.created_at = _dt_to_str(operator.created_at)
        row.updated_at = _dt_to_str(operator.updated_at) if operator.updated_at else None
        row.last_login_at = _dt_to_str(operator.last_login_at) if operator.last_login_at else None
        row.is_active = operator.is_active
        row.singleton_guard = 1
        try:
            self._session.flush()
        except IntegrityError as exc:
            if is_new:
                # A concurrent bootstrap already committed — the UNIQUE constraint on
                # singleton_guard (or username) fired.  Map deterministically to the
                # typed domain error so the router can return the correct 409.
                self._session.rollback()
                raise BootstrapAlreadyCompleted() from exc
            raise


class SqliteRevokedTokenRepository(RevokedTokenRepository):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def is_revoked(self, jti: str) -> bool:
        row = self._session.get(RevokedTokenORM, jti)
        return row is not None

    def save(self, revoked_token: RevokedToken) -> None:
        row = self._session.get(RevokedTokenORM, revoked_token.token_jti)
        if row is None:
            row = RevokedTokenORM(token_jti=revoked_token.token_jti)
            self._session.add(row)
        row.operator_id = revoked_token.operator_id
        row.revoked_at = _dt_to_str(revoked_token.revoked_at)
        row.expires_at = _dt_to_str(revoked_token.expires_at)
        row.reason = revoked_token.reason.value
        self._session.flush()

    def delete_expired(self, now: datetime) -> None:
        cutoff = _dt_to_str(now)
        self._session.query(RevokedTokenORM).filter(RevokedTokenORM.expires_at <= cutoff).delete()
        self._session.flush()


class SqliteThrottleStateRepository(ThrottleStateRepository):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_by_operator(self, operator_id: str) -> LoginThrottleState | None:
        row = self._session.get(LoginThrottleStateORM, operator_id)
        return _orm_to_throttle_state(row) if row else None

    def save(self, state: LoginThrottleState) -> None:
        row = self._session.get(LoginThrottleStateORM, state.operator_id)
        if row is None:
            row = LoginThrottleStateORM(operator_id=state.operator_id)
            self._session.add(row)
        row.failed_attempts = state.failed_attempts
        row.blocked_until = _dt_to_str(state.blocked_until) if state.blocked_until else None
        row.last_failed_at = _dt_to_str(state.last_failed_at) if state.last_failed_at else None
        self._session.flush()


class SqliteUnitOfWork(UnitOfWorkPort):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def commit(self) -> None:
        self._session.commit()
