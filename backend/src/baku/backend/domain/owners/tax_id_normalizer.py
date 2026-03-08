"""tax_id normalizer — deterministic normalization pipeline.

Pipeline: trim -> uppercase -> remove internal spaces -> remove hyphens.

Purpose: Prevent semantic duplicates caused by formatting variants,
ensuring uniqueness is enforced on the canonical form.
"""

from __future__ import annotations


def normalize_tax_id(raw: str) -> str:
    """Return the canonical form of a tax_id.

    Steps applied in order:
    1. Strip leading/trailing whitespace.
    2. Convert to uppercase.
    3. Remove all internal spaces.
    4. Remove all hyphens.
    """
    value = raw.strip()
    value = value.upper()
    value = value.replace(" ", "")
    value = value.replace("-", "")
    return value
