"""Application-layer port: authentication policy configuration (ADR-0002).

Infrastructure (AuthSettingsPolicy) implements this port.
Use cases depend only on this protocol — never on env vars directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AuthPolicyPort(ABC):
    @property
    @abstractmethod
    def token_ttl_seconds(self) -> int: ...

    @property
    @abstractmethod
    def max_failed_attempts(self) -> int: ...

    @property
    @abstractmethod
    def lockout_minutes(self) -> int: ...
