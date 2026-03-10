"""Typed property domain errors — stable codes in English, messages in Spanish.

HTTP status codes follow ADR-0009 and the properties contract (error-model.md).
"""

from __future__ import annotations


class PropertyError(Exception):
    """Base class for all property/ownership domain errors."""

    error_code: str = "PROPERTY_ERROR"
    message: str = "Error en la operación de propiedad."
    http_status: int = 400

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.message
        super().__init__(self.detail)


class PropertyNotFound(PropertyError):
    error_code = "PROPERTY_NOT_FOUND"
    message = "La propiedad no existe o no está disponible."
    http_status = 404


class PropertyAlreadyDeleted(PropertyNotFound):
    """Alias: same code and status as PROPERTY_NOT_FOUND."""

    pass


class PropertyValidationError(PropertyError):
    error_code = "VALIDATION_ERROR"
    message = "Los datos de la propiedad no son válidos."
    http_status = 400


class PropertyOwnershipRequired(PropertyError):
    error_code = "PROPERTY_OWNERSHIP_REQUIRED"
    message = "Se requiere al menos un titular para crear la propiedad."
    http_status = 400


class PropertyOwnershipSumExceeded(PropertyError):
    error_code = "PROPERTY_OWNERSHIP_SUM_EXCEEDED"
    message = "La suma de porcentajes de titularidad supera el 100%."
    http_status = 409


class PropertyDerivedFieldNotEditable(PropertyError):
    error_code = "PROPERTY_DERIVED_FIELD_NOT_EDITABLE"
    message = "Los campos derivados catastrales no son editables directamente."
    http_status = 400


class OwnershipDuplicateActivePair(PropertyError):
    error_code = "OWNERSHIP_DUPLICATE_ACTIVE_PAIR"
    message = "Ya existe una titularidad activa para este propietario en esta propiedad."
    http_status = 409


class OwnerNotFoundForOwnership(PropertyError):
    error_code = "OWNER_NOT_FOUND"
    message = "El propietario indicado no existe o no está disponible."
    http_status = 404
