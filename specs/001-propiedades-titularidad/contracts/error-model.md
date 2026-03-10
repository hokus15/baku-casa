# Error Model - F-0003 Propiedades y Titularidad

## Objetivo

Definir errores tipificados y su mapeo HTTP para operaciones de propiedades y titularidad,
alineado con ADR-0004 y ADR-0009.

## Reglas generales

- `error_code`: estable y en ingles.
- `message`: descriptivo y en espanol.
- `correlation_id`: obligatorio en toda respuesta de error.
- Sin exposicion de detalles internos de excepcion.

## Catalogo de errores

| error_code | HTTP | Escenario |
|---|---|---|
| `VALIDATION_ERROR` | 400 | Payload invalido, enum no permitido, formato fecha invalido, precision de porcentaje > 2 decimales |
| `PROPERTY_OWNERSHIP_REQUIRED` | 400 | Alta/actualizacion que deja propiedad activa sin titulares activos |
| `PROPERTY_OWNERSHIP_SUM_EXCEEDED` | 409 | Suma de `ownership_percentage` activa mayor que 100 |
| `PROPERTY_DERIVED_FIELD_NOT_EDITABLE` | 400 | Intento de editar `cadastral_construction_value` o `construction_ratio` |
| `OWNERSHIP_DUPLICATE_ACTIVE_PAIR` | 409 | Segunda titularidad activa para el mismo (`property_id`, `owner_id`) |
| `OWNER_NOT_FOUND` | 404 | Referencia a `owner_id` inexistente al asignar titularidad |
| `PROPERTY_NOT_FOUND` | 404 | `property_id` inexistente o no visible en contexto de consulta |
| `UNAUTHENTICATED` | 401 | Falta token, token invalido/expirado/revocado |
| `FORBIDDEN` | 403 | Operador autenticado sin autorizacion (reservado para evolucion de permisos) |
| `CONFLICT` | 409 | Conflicto de concurrencia o invariante no cubierto por codigo especifico |
| `INTERNAL_ERROR` | 500 | Error inesperado no funcional |

## Respuesta de error (contrato)

```json
{
  "error_code": "PROPERTY_OWNERSHIP_SUM_EXCEEDED",
  "message": "La suma de porcentajes de titularidad no puede superar 100.",
  "correlation_id": "a3f8a2b7d2f24f8f9b8f5a412f3d9a5e"
}
```

## Notas de consistencia

- `PROPERTY_NOT_FOUND` se utiliza tambien en delete idempotente funcional (segunda eliminacion sobre id inexistente/no activo).
- `VALIDATION_ERROR` cubre reglas de formato temporal: timestamps y fechas deben respetar contrato (`ISO-8601 UTC Z` y `YYYY-MM-DD`).
- El mapeo 409 se reserva para conflictos de invariante y concurrencia; validaciones de formato/enum permanecen en 400.
