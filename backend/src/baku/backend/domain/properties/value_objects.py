"""Property domain value objects — F-0003.

Ownership percentage rules follow ADR-0011 (0-100 scale, Decimal, max 2 decimals).
"""

from __future__ import annotations

from decimal import ROUND_DOWN, Decimal

_TWO_PLACES = Decimal("0.01")
_ZERO = Decimal("0")


def validate_ownership_percentage(value: Decimal) -> Decimal:
    """Validate that *value* is non-negative with at most 2 decimal places.

    Upper-bound (> 100) is intentionally *not* enforced here; the aggregate
    sum-check in policies.validate_ownership_inputs raises
    PropertyOwnershipSumExceeded (409) when the total exceeds 100.

    Raises ValueError if the value is negative or has excessive precision.
    Returns the normalised Decimal.
    """
    if value < _ZERO:
        raise ValueError(f"ownership_percentage must be >= 0, got {value}.")
    # Reject values with more than 2 decimal places
    quantised = value.quantize(_TWO_PLACES, rounding=ROUND_DOWN)
    if quantised != value:
        raise ValueError(
            f"ownership_percentage must have at most 2 decimal places, got {value}."
        )
    return value
