"""Domain repository ports (abstract interfaces) for properties — F-0003."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from baku.backend.domain.properties.entities import Ownership, Property


@dataclass
class PropertyPage:
    """Paginated result from property list queries."""

    items: list[Property]
    total: int
    page: int
    page_size: int


class PropertyRepository(ABC):
    @abstractmethod
    def find_by_id(
        self, property_id: str, include_deleted: bool = False
    ) -> Property | None: ...

    @abstractmethod
    def save(self, property_: Property) -> None: ...

    @abstractmethod
    def list(
        self,
        page: int,
        page_size: int,
        include_deleted: bool,
    ) -> PropertyPage: ...


class OwnershipRepository(ABC):
    @abstractmethod
    def find_active_by_pair(
        self, property_id: str, owner_id: str
    ) -> Ownership | None: ...

    @abstractmethod
    def list_active_by_property(self, property_id: str) -> list[Ownership]: ...

    @abstractmethod
    def list_active_by_owner(
        self,
        owner_id: str,
        page: int,
        page_size: int,
    ) -> PropertyPage: ...

    @abstractmethod
    def save(self, ownership: Ownership) -> None: ...

    @abstractmethod
    def save_all(self, ownerships: list[Ownership]) -> None: ...

    @abstractmethod
    def soft_delete_active_by_property(
        self, property_id: str, deleted_by: str, now: str
    ) -> None: ...


class PropertyUnitOfWorkPort(ABC):
    """Transaction boundary port for property write operations."""

    @abstractmethod
    def commit(self) -> None: ...
