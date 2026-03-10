# Quickstart - F-0003 Propiedades y Titularidad

## Objective

Validar end-to-end el alta, consulta, actualizacion y baja logica de propiedades,
asi como la gestion de titularidad actual con sus invariantes de porcentaje y auditoria.

## Preconditions

- Ejecutar en root `backend` con configuracion de entorno valida.
- Flujo de autenticacion de F-0001 operativo.
- Entidades de propietarios de F-0002 disponibles para asignacion de titularidad.
- Estado de base de datos controlado para validaciones deterministas.

## Manual validation flow

1. Autenticar operador
  - Obtener JWT valido y usarlo en todos los requests.

2. Crear propiedad con titularidad inicial
  - Crear propiedad con `name`, `type` valido y al menos una titularidad.
  - Verificar respuesta 201 y presencia de metadatos de auditoria.
  - Verificar que no se serializan campos opcionales en `null`.

3. Validar invariantes de titularidad
  - Probar `ownership_percentage` fuera de rango y con mas de 2 decimales.
  - Probar suma > 100 y verificar rechazo.
  - Probar suma <= 100 y verificar aceptacion.
  - Probar duplicidad activa de (`property_id`, `owner_id`) y verificar conflicto.

4. Validar campos derivados catastrales
  - Enviar datos catastrales base y verificar calculo de derivados en salida.
  - Intentar editar directamente derivados y verificar rechazo tipificado.

5. Consultas funcionales
  - Obtener detalle de propiedad.
  - Listar propiedades con paginacion (`page`, `page_size`).
  - Consultar propietarios por propiedad.
  - Consultar propiedades por propietario.

6. Soft-delete de propiedad
  - Eliminar propiedad y verificar respuesta 204.
  - Confirmar que propiedad y titularidades asociadas no aparecen en consultas activas.
  - Verificar presencia de `deleted_at` y `deleted_by` en almacenamiento.

7. Contrato temporal
  - Verificar `timestamps` en ISO-8601 UTC con `Z`.
  - Verificar fechas puras en `YYYY-MM-DD`.

8. Errores y observabilidad
  - Verificar errores tipificados con `error_code`, `message`, `correlation_id`.
  - Verificar logs estructurados con `correlation_id` y sin secretos/PII por defecto.

## Contract and CI validation

Quality gates esperados para este slice:

- `ruff check src/ tests/`
- `mypy src/`
- `pytest tests/ -q`

Cobertura minima de contract tests:

- create property (201) y validaciones de payload (400)
- owner inexistente en titularidad (404)
- suma de porcentaje > 100 (409)
- precision de porcentaje > 2 decimales (400)
- duplicidad activa de par (`property_id`, `owner_id`) (409)
- listados paginados con defaults y limites
- consulta por propietario y por propiedad
- soft-delete con cascada y exclusion de consultas activas
- rechazo de acceso no autenticado (401)
