"""Owner domain value objects — EntityType enumeration."""

from __future__ import annotations

from enum import Enum


class EntityType(str, Enum):
    PERSONA_FISICA = "PERSONA_FISICA"
    PERSONA_JURIDICA = "PERSONA_JURIDICA"
    ESPJ = "ESPJ"
