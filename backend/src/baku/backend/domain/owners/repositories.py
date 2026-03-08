"""Domain repository ports (abstract interfaces) for owners — F-0002."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from baku.backend.domain.owners.entities import Owner


@dataclass
class OwnerPage:
    """Paginated result from list queries."""

    items: list[Owner]
    total: int
    page: int
    page_size: int


class OwnerRepository(ABC):
    @abstractmethod
    def find_by_id(self, owner_id: str, include_deleted: bool = False) -> Owner | None: ...

    @abstractmethod
    def find_by_tax_id(self, normalized_tax_id: str, exclude_owner_id: str | None = None) -> Owner | None:
        """Find active owner by normalized tax_id, optionally excluding a specific owner_id."""
        ...

    @abstractmethod
    def save(self, owner: Owner) -> None: ...

    @abstractmethod
    def list(
        self,
        page: int,
        page_size: int,
        tax_id: str | None,
        legal_name: str | None,
        include_deleted: bool,
    ) -> OwnerPage: ...


class OwnerUnitOfWorkPort(ABC):
    """Transaction boundary port for owner write operations."""

    @abstractmethod
    def commit(self) -> None: ...
