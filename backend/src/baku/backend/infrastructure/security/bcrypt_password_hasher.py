"""Bcrypt implementation of PasswordHasherPort (ADR-0002)."""

from __future__ import annotations

import bcrypt

from baku.backend.application.auth.password_hasher_port import PasswordHasherPort


class BcryptPasswordHasher(PasswordHasherPort):
    def hash(self, plain: str) -> str:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    def verify(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
