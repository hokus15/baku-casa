"""Domain repository ports (abstract interfaces) for authentication."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from baku.backend.domain.auth.entities import LoginThrottleState, Operator, RevokedToken


class OperatorRepository(ABC):
    @abstractmethod
    def find_active(self) -> Operator | None: ...

    @abstractmethod
    def find_by_username(self, username: str) -> Operator | None: ...

    @abstractmethod
    def save(self, operator: Operator) -> None: ...


class RevokedTokenRepository(ABC):
    @abstractmethod
    def is_revoked(self, jti: str) -> bool: ...

    @abstractmethod
    def save(self, revoked_token: RevokedToken) -> None: ...

    @abstractmethod
    def delete_expired(self, now: datetime) -> None: ...


class ThrottleStateRepository(ABC):
    @abstractmethod
    def find_by_operator(self, operator_id: str) -> LoginThrottleState | None: ...

    @abstractmethod
    def save(self, state: LoginThrottleState) -> None: ...
