"""Application-layer port: password hashing (ADR-0002).

Infrastructure (BcryptPasswordHasher) implements this port.
Use cases depend only on this ABC — never on bcrypt directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PasswordHasherPort(ABC):
    @abstractmethod
    def hash(self, plain: str) -> str: ...

    @abstractmethod
    def verify(self, plain: str, hashed: str) -> bool: ...
