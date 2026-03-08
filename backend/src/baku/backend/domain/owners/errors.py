"""Typed owner domain errors — stable codes in English, messages in Spanish.

HTTP status codes follow ADR-0009 and the owners contract (error-model.md).
"""

from __future__ import annotations


class OwnerError(Exception):
    """Base class for all owner domain errors."""

    error_code: str = "OWNER_ERROR"
    message: str = "Error en la operación de propietario."
    http_status: int = 400

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.message
        super().__init__(self.detail)


class OwnerNotFound(OwnerError):
    error_code = "OWNER_NOT_FOUND"
    message = "El propietario no existe o no está disponible."
    http_status = 404


class OwnerAlreadyDeleted(OwnerError):
    error_code = "OWNER_ALREADY_DELETED"
    message = "El propietario ya ha sido eliminado."
    http_status = 404


class OwnerTaxIdConflict(OwnerError):
    error_code = "OWNER_TAX_ID_CONFLICT"
    message = "Ya existe un propietario activo con ese identificador fiscal."
    http_status = 409


class OwnerValidationError(OwnerError):
    error_code = "OWNER_VALIDATION_ERROR"
    message = "Los datos del propietario no son válidos."
    http_status = 400


class OwnerImmutableId(OwnerError):
    error_code = "OWNER_IMMUTABLE_ID"
    message = "El identificador del propietario no puede modificarse."
    http_status = 400
