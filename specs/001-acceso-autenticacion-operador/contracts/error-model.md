# Error Contract — Authentication (F-0001)

## Reglas generales

- `error_code`: estable, en inglés.
- `message`: orientado a usuario, en español.
- `correlation_id`: obligatorio en toda respuesta de error.

## Códigos de error funcionales previstos

- `AUTH_BOOTSTRAP_ALREADY_COMPLETED`
- `AUTH_INVALID_CREDENTIALS`
- `AUTH_TOKEN_EXPIRED`
- `AUTH_TOKEN_REVOKED`
- `AUTH_TOKEN_INVALID`
- `AUTH_LOCKED_TEMPORARILY`
- `AUTH_PASSWORD_CHANGE_REQUIRES_AUTH`
- `AUTH_FORBIDDEN`

## Mapeo HTTP esperado

- `400`: validación de payload de autenticación
- `401`: no autenticado / token inválido-expirado-revocado / credenciales inválidas
- `403`: acceso prohibido por estado no permitido
- `409`: conflicto de estado (ej. bootstrap repetido)
