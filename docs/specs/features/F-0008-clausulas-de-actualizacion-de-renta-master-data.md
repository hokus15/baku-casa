# F-0008: Cláusulas de Actualización de Renta (Master Data)

---

## Objetivo

Permitir definir cláusulas de actualización de renta asociadas a un contrato, representando reglas independientes del histórico que determinan cuándo y cómo debe actualizarse la renta en el tiempo.

Estas cláusulas no modifican automáticamente la renta en esta feature, sino que establecen la configuración necesaria para futuras actualizaciones automatizadas o asistidas.

---

## Alcance

- Persistencia estructural de reglas de actualización.
- Uso del mismo `update_type` definido en Feature 5.
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

## Definiciones

- **Cláusula de actualización**: regla contractual que define la recurrencia y el mecanismo de actualización de la renta.
- **Recurrencia (rrule)**: regla que determina cuándo debe evaluarse la actualización.
- **Tipo de actualización**: valor perteneciente a la misma lista interna definida en Feature 5 (histórico de rentas).
- **Parámetros de actualización**: conjunto de campos adicionales requeridos según el tipo de actualización.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Cláusula de actualización
- Recurrencia (rrule)

---

## Datos principales

La feature gestiona la siguiente información:

### Entidad

### RentUpdateClause

**Campos obligatorios**

- `contract_id`
- `update_type`
- `rrule`

**Campos opcionales (según tipo)**

- `fixed_percent`
- `fixed_amount`
- `min_limit`
- `max_limit`
- `reference_index`
- `rounding_rule`
- Otros parámetros específicos definidos por cada tipo

### Auditoría y soft delete

Esta feature reutiliza el contrato común definido en:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md

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

Los listados y consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md.

---

## Reglas del dominio

1. Un contrato puede tener 0..N cláusulas de actualización.
2. Cada cláusula debe tener `update_type` y `rrule`.
3. `update_type` debe pertenecer a la lista interna del sistema.
4. La lista de tipos es extensible y no cerrada a nivel de dominio (permitiendo ampliaciones futuras).
5. Los parámetros requeridos dependen del `update_type`.
6. Si un tipo requiere parámetros específicos, estos deben validarse como obligatorios.
7. Las cláusulas son independientes del histórico de rentas.
8. La existencia de una cláusula no implica modificación automática de la renta.
9. Se permite más de una cláusula activa en el mismo contrato.
10. El modelo debe permitir ampliar los tipos y parámetros de actualización sin romper cláusulas ya existentes.
11. La eliminación de cláusulas debe seguir la semántica compartida de soft delete definida en docs/specs/shared/SHARED-0001-audit-and-soft-delete.md.

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Un contrato puede tener 0..N cláusulas de actualización.
- Cada cláusula debe tener `update_type` y `rrule`.
- `update_type` debe pertenecer a la lista interna del sistema.

---

## Dependencias

Esta feature puede depender de:

- F-0006

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
- docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- Crear cláusula de actualización asociada a un contrato.
- Editar cláusula.
- Eliminar cláusula (soft delete).

---

