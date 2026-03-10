"""Domain policies for property ownership invariants — F-0003.

Validates business rules that span multiple entities or require
aggregate-level reasoning (ownership sum, unique active pairs, etc.).
"""

from __future__ import annotations

from decimal import Decimal

from baku.backend.domain.properties.errors import (
    OwnershipDuplicateActivePair,
    PropertyOwnershipSumExceeded,
    PropertyValidationError,
)
from baku.backend.domain.properties.value_objects import validate_ownership_percentage

_MAX_SUM = Decimal("100")


def validate_ownership_inputs(
    ownerships: list[tuple[str, Decimal]],
) -> None:
    """Validate a list of (owner_id, percentage) pairs for a property operation.

    Raises:
        PropertyValidationError: if any percentage has invalid precision/range.
        OwnershipDuplicateActivePair: if the same owner_id appears more than once.
        PropertyOwnershipSumExceeded: if the total exceeds 100.
    """
    seen_owner_ids: set[str] = set()
    total = Decimal("0")

    for owner_id, percentage in ownerships:
        try:
            validate_ownership_percentage(percentage)
        except ValueError as exc:
            raise PropertyValidationError(str(exc)) from exc

        if owner_id in seen_owner_ids:
            raise OwnershipDuplicateActivePair()
        seen_owner_ids.add(owner_id)
        total += percentage

    if total > _MAX_SUM:
        raise PropertyOwnershipSumExceeded()


def check_derived_fields_not_in_update(update_kwargs: dict) -> None:
    """Raise PropertyDerivedFieldNotEditable if any derived field is present in the update."""
    from baku.backend.domain.properties.errors import PropertyDerivedFieldNotEditable

    _DERIVED_FIELDS = {"cadastral_construction_value", "construction_ratio"}
    for field in _DERIVED_FIELDS:
        if field in update_kwargs and update_kwargs[field] is not None:
            raise PropertyDerivedFieldNotEditable(
                f"Field '{field}' is derived and cannot be set directly."
            )
