"""Password hasher — bcrypt direct (no passlib). Infrastructure layer only."""
from __future__ import annotations

import bcrypt


def hash_password(plain: str) -> str:
    """Return bcrypt hash of the given password. Never stores plain text."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if plain matches the bcrypt hash."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())
