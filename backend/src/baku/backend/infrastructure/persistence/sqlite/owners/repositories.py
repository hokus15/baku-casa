"""SQLite repositories for owners — infrastructure layer.

Uniqueness of tax_id among active records is enforced at the application layer
by calling find_by_tax_id before save, so no DB unique constraint is required
(SQLite lacks partial unique indexes on filtered expressions before 3.32).
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from baku.backend.domain.owners.entities import Owner
from baku.backend.domain.owners.repositories import OwnerPage, OwnerRepository, OwnerUnitOfWorkPort
from baku.backend.infrastructure.persistence.sqlite.owners.mappers import orm_to_owner, owner_to_orm
from baku.backend.infrastructure.persistence.sqlite.owners.models import OwnerORM

_MAX_PAGE_SIZE = 100


class SqliteOwnerRepository(OwnerRepository):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_by_id(self, owner_id: str, include_deleted: bool = False) -> Owner | None:
        row = self._session.get(OwnerORM, owner_id)
        if row is None:
            return None
        if not include_deleted and row.deleted_at is not None:
            return None
        return orm_to_owner(row)

    def find_by_tax_id(self, normalized_tax_id: str, exclude_owner_id: str | None = None) -> Owner | None:
        query = (
            self._session.query(OwnerORM)
            .filter(OwnerORM.tax_id == normalized_tax_id)
            .filter(OwnerORM.deleted_at.is_(None))
        )
        if exclude_owner_id is not None:
            query = query.filter(OwnerORM.owner_id != exclude_owner_id)
        row = query.first()
        return orm_to_owner(row) if row else None

    def save(self, owner: Owner) -> None:
        existing = self._session.get(OwnerORM, owner.owner_id)
        row = owner_to_orm(owner, existing)
        if existing is None:
            self._session.add(row)
        self._session.flush()

    def list(
        self,
        page: int,
        page_size: int,
        tax_id: str | None,
        legal_name: str | None,
        include_deleted: bool,
    ) -> OwnerPage:
        capped_size = min(page_size, _MAX_PAGE_SIZE)
        query = self._session.query(OwnerORM)

        if not include_deleted:
            query = query.filter(OwnerORM.deleted_at.is_(None))

        if tax_id is not None:
            query = query.filter(OwnerORM.tax_id == tax_id)

        if legal_name is not None:
            query = query.filter(OwnerORM.legal_name.ilike(f"%{legal_name}%"))

        total = query.count()
        offset = (page - 1) * capped_size
        rows = query.order_by(OwnerORM.created_at.asc()).offset(offset).limit(capped_size).all()

        return OwnerPage(
            items=[orm_to_owner(r) for r in rows],
            total=total,
            page=page,
            page_size=capped_size,
        )


class SqliteOwnerUnitOfWork(OwnerUnitOfWorkPort):  # type: ignore[misc]
    def __init__(self, session: Session) -> None:
        self._session = session

    def commit(self) -> None:
        self._session.commit()
