"""Domain entities for F-0001 authentication — pure Python, no framework dependencies."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class RevocationReason(str, Enum):
    LOGOUT = "logout"


@dataclass
class Operator:
    """Single authenticated operator of the system."""

    operator_id: str
    username: str
    password_hash: str
    credential_version: int
    created_at: datetime
    is_active: bool
    updated_at: datetime | None = None
    last_login_at: datetime | None = None

    @staticmethod
    def new(username: str, password_hash: str, now: datetime) -> "Operator":
        """Create a fresh operator from bootstrap. credential_version starts at 1."""
        return Operator(
            operator_id=str(uuid.uuid4()),
            username=username,
            password_hash=password_hash,
            credential_version=1,
            created_at=now,
            is_active=True,
        )

    def rotate_password(self, new_hash: str, now: datetime) -> None:
        """Increment credential_version atomically and update hash. Invalidates prior tokens."""
        self.password_hash = new_hash
        self.credential_version += 1
        self.updated_at = now

    def record_login(self, now: datetime) -> None:
        self.last_login_at = now


@dataclass
class RevokedToken:
    """Explicit per-token revocation record, created on logout."""

    token_jti: str
    operator_id: str
    revoked_at: datetime
    expires_at: datetime
    reason: RevocationReason

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at


@dataclass
class LoginThrottleState:
    """Tracks failed login attempts and temporary lockout for an operator."""

    operator_id: str
    failed_attempts: int = field(default=0)
    blocked_until: datetime | None = field(default=None)
    last_failed_at: datetime | None = field(default=None)

    def is_blocked(self, now: datetime) -> bool:
        return self.blocked_until is not None and now < self.blocked_until

    def record_failure(
        self, now: datetime, max_attempts: int, lockout_minutes: int
    ) -> None:
        self.failed_attempts += 1
        self.last_failed_at = now
        if self.failed_attempts >= max_attempts:
            self.blocked_until = now + timedelta(minutes=lockout_minutes)

    def record_success(self) -> None:
        self.failed_attempts = 0
        self.blocked_until = None
        self.last_failed_at = None
