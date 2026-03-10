"""SQLite repositories for properties and ownerships — infrastructure layer.

Active-pair uniqueness of (property_id, owner_id) is enforced at the application
layer (find_active_by_pair before save) to handle soft-deleted pairs correctly.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from baku.backend.domain.properties.entities import Ownership, Property
from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyPage,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)
from baku.backend.infrastructure.persistence.sqlite.properties.mappers import (
    orm_to_ownership,
    orm_to_property,
    ownership_to_orm,
    property_to_orm,
)
from baku.backend.infrastructure.persistence.sqlite.properties.models import (
    OwnershipORM,
    PropertyORM,
)


class SqlitePropertyRepository(PropertyRepository):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_by_id(
        self, property_id: str, include_deleted: bool = False
    ) -> Property | None:
        row = self._session.get(PropertyORM, property_id)
        if row is None:
            return None
        if not include_deleted and row.deleted_at is not None:
            return None
        return orm_to_property(row)

    def save(self, property_: Property) -> None:
        existing = self._session.get(PropertyORM, property_.property_id)
        row = property_to_orm(property_, existing)
        if existing is None:
            self._session.add(row)
        self._session.flush()

    def list(
        self,
        page: int,
        page_size: int,
        include_deleted: bool,
    ) -> PropertyPage:
        query = self._session.query(PropertyORM)
        if not include_deleted:
            query = query.filter(PropertyORM.deleted_at.is_(None))
        total = query.count()
        offset = (page - 1) * page_size
        rows = (
            query.order_by(PropertyORM.created_at.asc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return PropertyPage(
            items=[orm_to_property(r) for r in rows],
            total=total,
            page=page,
            page_size=page_size,
        )


class SqliteOwnershipRepository(OwnershipRepository):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_active_by_pair(
        self, property_id: str, owner_id: str
    ) -> Ownership | None:
        row = (
            self._session.query(OwnershipORM)
            .filter(
                OwnershipORM.property_id == property_id,
                OwnershipORM.owner_id == owner_id,
                OwnershipORM.deleted_at.is_(None),
            )
            .first()
        )
        return orm_to_ownership(row) if row else None

    def list_active_by_property(self, property_id: str) -> list[Ownership]:
        rows = (
            self._session.query(OwnershipORM)
            .filter(
                OwnershipORM.property_id == property_id,
                OwnershipORM.deleted_at.is_(None),
            )
            .order_by(OwnershipORM.created_at.asc())
            .all()
        )
        return [orm_to_ownership(r) for r in rows]

    def list_active_by_owner(
        self,
        owner_id: str,
        page: int,
        page_size: int,
    ) -> PropertyPage:
        """Return a paginated list of active properties for a given owner_id."""
        # Sub-select the distinct property_ids owned by this owner
        subquery = select(OwnershipORM.property_id).where(
            OwnershipORM.owner_id == owner_id,
            OwnershipORM.deleted_at.is_(None),
        )
        query = self._session.query(PropertyORM).filter(
            PropertyORM.property_id.in_(subquery),
            PropertyORM.deleted_at.is_(None),
        )
        total = query.count()
        offset = (page - 1) * page_size
        rows = (
            query.order_by(PropertyORM.created_at.asc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return PropertyPage(
            items=[orm_to_property(r) for r in rows],
            total=total,
            page=page,
            page_size=page_size,
        )

    def save(self, ownership: Ownership) -> None:
        existing = self._session.get(OwnershipORM, ownership.ownership_id)
        row = ownership_to_orm(ownership, existing)
        if existing is None:
            self._session.add(row)
        self._session.flush()

    def save_all(self, ownerships: list[Ownership]) -> None:
        for ownership in ownerships:
            self.save(ownership)

    def soft_delete_active_by_property(
        self, property_id: str, deleted_by: str, now: str
    ) -> None:
        (
            self._session.query(OwnershipORM)
            .filter(
                OwnershipORM.property_id == property_id,
                OwnershipORM.deleted_at.is_(None),
            )
            .update(
                {"deleted_at": now, "deleted_by": deleted_by},
                synchronize_session="fetch",
            )
        )


class SqlitePropertyUnitOfWork(PropertyUnitOfWorkPort):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def commit(self) -> None:
        self._session.commit()
