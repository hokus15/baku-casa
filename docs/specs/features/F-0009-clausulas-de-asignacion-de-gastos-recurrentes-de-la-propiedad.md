# F-0009: Cláusulas de asignacion de gastos recurrentes de la propiedad

---

## Objetivo

Permitir que un contrato defina la reasignación de responsabilidad de uno o varios gastos recurrentes operativos de la propiedad al inquilino.

Estas cláusulas no crean nuevos gastos, sino que modifican quién asume económicamente los gastos ya definidos como plantillas en la propiedad.

---

## Alcance

- Reasignación estructural de responsabilidad.
- Asociación exclusiva a gastos ya existentes en la propiedad.
- Soporte de múltiples gastos por contrato.
- Soporte opcional de rango temporal de vigencia.
- Preparado para futura imputación automática de cargos.

---

## Fuera de alcance

- Creación automática de nuevos gastos.
- Generación automática de cargos al inquilino.
- Reparto parcial del gasto entre propietario e inquilino.
- Cálculo contable o fiscal derivado.
- Gestión de responsabilidad compartida.

---

## Definiciones

- **Gasto recurrente operativo**: plantilla de gasto definida a nivel de propiedad.
- **Cláusula de responsabilidad**: regla contractual que determina que el inquilino asume el pago de un gasto recurrente existente.
- **Reasignación de responsabilidad**: cambio del obligado al pago (propietario → inquilino), sin alterar la existencia del gasto.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Gasto recurrente operativo
- Cláusula de responsabilidad

---

## Datos principales

La feature gestiona la siguiente información:

### Entidad

### ExpenseResponsibilityClause

**Campos obligatorios**

- `contract_id`
- `property_recurring_expense_template_id`

**Campos opcionales**

- `start_date`
- `end_date`
- `notes`

### Auditoría y soft delete

Esta feature reutiliza el contrato común definido en:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md

**Relaciones**

- 1 LeaseContract → 0..N ExpenseResponsibilityClause
- 1 RecurringExpenseTemplate → 0..N ExpenseResponsibilityClause

---

## Capacidades

- Asociar uno o varios gastos recurrentes de la propiedad a un contrato como responsabilidad del inquilino.
- Editar cláusula.
- Eliminar cláusula (soft delete).
- Listar cláusulas de responsabilidad de un contrato.
- Determinar, para una fecha dada, si un gasto es responsabilidad del propietario o del inquilino.

---

Los listados y consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md.

---

## Reglas del dominio

1. Un contrato puede tener 0..N cláusulas de responsabilidad.
2. Solo pueden referenciarse gastos recurrentes existentes en la propiedad.
3. La cláusula no crea un nuevo gasto; solo reasigna la responsabilidad.
4. Un mismo gasto recurrente no puede estar duplicado en cláusulas activas para el mismo contrato con rangos solapados.
5. Si se define `start_date` y `end_date`, deben respetar coherencia temporal (`end_date ≥ start_date`).
6. La responsabilidad efectiva en una fecha se determina evaluando:
   - vigencia del contrato
   - vigencia de la plantilla de gasto
   - vigencia de la cláusula
7. La eliminación debe seguir la semántica compartida de soft delete definida en docs/specs/shared/SHARED-0001-audit-and-soft-delete.md.
8. En ausencia de cláusula activa, el gasto se considera responsabilidad del propietario.
---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Un contrato puede tener 0..N cláusulas de responsabilidad.
- Solo pueden referenciarse gastos recurrentes existentes en la propiedad.
- La cláusula no crea un nuevo gasto; solo reasigna la responsabilidad.

---

## Dependencias

Esta feature puede depender de:

- F-0005
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

- Asociar uno o varios gastos recurrentes de la propiedad a un contrato como responsabilidad del inquilino.
- Editar cláusula.
- Eliminar cláusula (soft delete).

---

