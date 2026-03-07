# F-0008: Cláusulas de Actualización de Renta (Master Data)

## Objetivo

Permitir definir cláusulas de actualización de renta asociadas a un contrato, representando reglas independientes del histórico que determinan cuándo y cómo debe actualizarse la renta en el tiempo.

Estas cláusulas no modifican automáticamente la renta en esta feature, sino que establecen la configuración necesaria para futuras actualizaciones automatizadas o asistidas.

---

## Definiciones

- **Cláusula de actualización**: regla contractual que define la recurrencia y el mecanismo de actualización de la renta.
- **Recurrencia (rrule)**: regla que determina cuándo debe evaluarse la actualización.
- **Tipo de actualización**: valor perteneciente a la misma lista interna definida en Feature 5 (histórico de rentas).
- **Parámetros de actualización**: conjunto de campos adicionales requeridos según el tipo de actualización.

---

## Entidad

### RentUpdateClause

**Campos obligatorios**

- `contract_id`
- `tipo_actualizacion`
- `rrule`

**Campos opcionales (según tipo)**

- `porcentaje_fijo`
- `cantidad_fija`
- `limite_minimo`
- `limite_maximo`
- `indice_referencia`
- `redondeo`
- Otros parámetros específicos definidos por cada tipo

### Auditoría

- `created_at`
- `created_by`
- `updated_at`
- `updated_by`
- `deleted_at` (nullable)
- `deleted_by` (nullable)

La eliminación es lógica y auditable.

**Relación**

- 1 LeaseContract → 0..N RentUpdateClause

---

## Capacidades

- Crear cláusula de actualización asociada a un contrato.
- Editar cláusula.
- Eliminar cláusula (soft delete).
- Listar cláusulas de un contrato.
- Validar coherencia estructural según tipo.
- Permitir múltiples cláusulas independientes por contrato.

---

## Alcance

- Persistencia estructural de reglas de actualización.
- Uso del mismo `tipo_actualizacion` definido en Feature 5.
- Validación estructural de `rrule`.
- Validación de parámetros obligatorios según tipo.
- Diseño extensible para nuevos tipos de actualización.

---

## Fuera de alcance

- Ejecución automática de la actualización.
- Cálculo del nuevo importe de renta.
- Obtención automática de índices oficiales.
- Resolución de conflictos entre cláusulas.
- Simulación de escenarios futuros.

---

## Reglas de negocio

1. Un contrato puede tener 0..N cláusulas de actualización.
2. Cada cláusula debe tener `tipo_actualizacion` y `rrule`.
3. `tipo_actualizacion` debe pertenecer a la lista interna del sistema.
4. La lista de tipos es extensible y no cerrada a nivel de dominio (permitiendo ampliaciones futuras).
5. Los parámetros requeridos dependen del `tipo_actualizacion`.
6. Si un tipo requiere parámetros específicos, estos deben validarse como obligatorios.
7. Las cláusulas son independientes del histórico de rentas.
8. La existencia de una cláusula no implica modificación automática de la renta.
9. Se permite más de una cláusula activa en el mismo contrato.
10. El diseño debe permitir mapear cada `tipo_actualizacion` interno a un tipo definido en una librería externa.
11. La eliminación de cláusulas debe ser lógica (soft delete).

---

---

## Dependencias y trazabilidad

### Depende de
- F-0005

### Impacto en contratos
- HTTP API: (si aplica)
- Eventos (CloudEvents): (si aplica)

---

## ADR aplicables

### Base
- ADR-0001
- ADR-0002
- ADR-0003
- ADR-0004
- ADR-0005
- ADR-0006
- ADR-0007
- ADR-0008
- ADR-0009
- ADR-0011
- ADR-0012


---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Correlacion por request mediante `correlation_id`.
