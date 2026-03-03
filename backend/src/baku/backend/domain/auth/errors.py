"""Typed authentication domain errors — stable codes in English, messages in Spanish."""
from __future__ import annotations


class AuthError(Exception):
    """Base class for all authentication errors."""

    error_code: str = "AUTH_ERROR"
    message: str = "Error de autenticación."
    http_status: int = 400

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.message
        super().__init__(self.detail)


class BootstrapAlreadyCompleted(AuthError):
    error_code = "AUTH_BOOTSTRAP_ALREADY_COMPLETED"
    message = "El sistema ya ha sido inicializado. El bootstrap no puede ejecutarse nuevamente."
    http_status = 409


class InvalidCredentials(AuthError):
    error_code = "AUTH_INVALID_CREDENTIALS"
    message = "Las credenciales proporcionadas son inválidas."
    http_status = 401


class TokenExpired(AuthError):
    error_code = "AUTH_TOKEN_EXPIRED"
    message = "El token ha expirado. Por favor inicie sesión nuevamente."
    http_status = 401


class TokenRevoked(AuthError):
    error_code = "AUTH_TOKEN_REVOKED"
    message = "El token ha sido revocado."
    http_status = 401


class TokenInvalid(AuthError):
    error_code = "AUTH_TOKEN_INVALID"
    message = "El token no es válido."
    http_status = 401


class LockedTemporarily(AuthError):
    error_code = "AUTH_LOCKED_TEMPORARILY"
    message = (
        "La cuenta está bloqueada temporalmente por múltiples intentos fallidos. "
        "Por favor intente nuevamente más tarde."
    )
    http_status = 429


class PasswordChangeRequiresAuth(AuthError):
    error_code = "AUTH_PASSWORD_CHANGE_REQUIRES_AUTH"
    message = "El cambio de contraseña requiere autenticación válida."
    http_status = 401


class AuthForbidden(AuthError):
    error_code = "AUTH_FORBIDDEN"
    message = "No tiene permiso para realizar esta acción."
    http_status = 403
