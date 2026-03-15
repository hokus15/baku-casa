# F-0014: Automatización: Creación de Tareas

---

## Objetivo

Generar automáticamente tareas (F-0013) a partir del master data del sistema (rentas, gastos recurrentes, cláusulas de actualización de renta, preavisos) y de eventos del sistema duraderos (p.ej. creación de devengos facturables), para supervisión previa a la creación de devengos u otras entidades.

El sistema no ejecuta acciones automáticamente. La ejecución depende del cliente que consume la tarea.

---

## Alcance

Esta feature cubre el comportamiento funcional descrito en las secciones de datos, capacidades y reglas del dominio de esta especificación.

---

## Fuera de alcance

- Motor de workflows.
- Ejecución automática sin supervisión.
- Notificaciones externas.
- Cálculo automático de índices oficiales.

---

## Definiciones

- **Automatización**: regla que genera tareas cuando se cumple una condición temporal o un evento del sistema.
- **Evento del sistema duradero**: evento del dominio persistido y publicado mediante la capacidad transversal definida por EN-0208 cuando el disparador de automatización depende de publicación fiable.
- **Evento de automatización**: combinación única de:
  - tipo de automatización
  - entidad origen
  - periodo u ocurrencia concreta
- **Idempotencia**: garantía de que un mismo evento de automatización genera una única tarea, siguiendo el contrato común definido en docs/specs/shared/SHARED-0005-idempotency-contract.md.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Automatización
- Evento de automatización

---

## Datos principales

La feature gestiona la siguiente información:

### Tipos de tarea (task_type)

### RENT_ACCRUAL_PROPOSED
Propuesta de creación de devengo de renta mensual.

### RECURRING_EXPENSE_ACCRUAL_PROPOSED
Propuesta de creación de devengo por gasto recurrente.

### RENT_UPDATE_REVIEW
Revisión de actualización de renta según cláusula.

### CONTRACT_NOTICE_REMINDER
Recordatorio de preaviso contractual.

### INVOICE_DRAFT_PROPOSED
Propuesta de creación de factura en borrador (DRAFT) a partir de devengo(s) facturable(s).

### MANUAL
Tarea creada manualmente.

---

### Disparadores de automatización

### A1 — Renta mensual

Se genera una tarea cuando se cumple el día de cobro del contrato.

Regla de fecha:
- `charge_day_of_month`
- Si el día no existe en el mes → último día válido anterior.

Contexto mínimo:
- `contract_id`
- `property_id`
- `service_period_start`
- `service_period_end`
- `accrual_proposal`:
  - `type=INCOME`
  - `payer=TENANT`
  - `category`
  - `base_amount`
  - `accrual_date`
  - `due_date`
  - `vat_rate_percent`
  - `withholding_rate_percent`

---

### A2 — Gasto recurrente

Se genera una tarea cuando se cumple el `rrule` de la plantilla.

Determinación de pagador:
- Si existe contrato vigente y cláusula de responsabilidad activa → `payer=TENANT`
- En otro caso → `payer=OWNER`

Contexto mínimo:
- `property_id`
- `recurring_expense_template_id`
- `occurrence_date`
- `accrual_proposal`:
  - `type=EXPENSE`
  - `payer`
  - `category`
  - `base_amount`
  - `accrual_date`
  - `due_date`
  - `contract_id` si `payer=TENANT`

---

### A3 — Actualización de renta

Se genera una tarea cuando se cumple el `rrule` de una cláusula.

Contexto mínimo:
- `contract_id`
- `rent_update_clause_id`
- `occurrence_date`
- `rent_update_proposal`:
  - `update_type`
  - parámetros de la cláusula

---

### A4 — Preaviso contractual

Se genera una tarea cuando se cumple la fecha:

`effective_end_date - termination_notice_period`

Considerando prórrogas automáticas.

Contexto mínimo:
- `contract_id`
- `effective_end_date`
- `termination_notice_period`

---

### A5 — Facturación: devengo facturable creado

Se genera una tarea cuando se crea un devengo facturable.

Criterio:
- `vat_rate_percent > 0`

Contexto mínimo:
- `contract_id`
- `property_id`
- `invoice_proposal`:
  - `issue_date`
  - `lines`:
    - `accrual_id`
    - `description`
    - `base_amount`
    - `vat_rate_percent`
    - `withholding_rate_percent`
    - `service_period_start`
    - `service_period_end`

Idempotencia:
- `automation_key` debe ser único por devengo facturable (p.ej. `INVOICE_DRAFT_PROPOSED:<accrual_id>`).
- `automation_key` reutiliza el contrato común definido en docs/specs/shared/SHARED-0005-idempotency-contract.md.

---

## Capacidades

El sistema debe permitir:

- Generar tareas automáticamente a partir de reglas temporales definidas sobre contratos, cláusulas y gastos recurrentes.
- Generar tareas automáticamente a partir de eventos del sistema cuando el disparador sea durable y esté soportado por EN-0208.
- Incluir en cada tarea automática el contexto mínimo necesario para que el cliente pueda revisar y ejecutar la acción propuesta.
- Garantizar que una misma ocurrencia lógica de automatización produzca como máximo una tarea.

## Reglas del dominio

1. Las automatizaciones se evalúan por calendario (A1–A4) o por eventos del sistema (A5).
2. Cada evento de automatización debe generar una única tarea.
3. Debe existir una clave de idempotencia (`automation_key`) asociada al evento, siguiendo el contrato común definido en docs/specs/shared/SHARED-0005-idempotency-contract.md.
4. Las tareas automáticas deben incluir en su contexto toda la información necesaria para ejecutar la acción.
5. La creación de una tarea no implica ejecución automática.
6. La ejecución debe ser segura ante reintentos (no crear duplicados), conforme al contrato común definido en docs/specs/shared/SHARED-0005-idempotency-contract.md.
7. El sistema debe permitir añadir nuevas automatizaciones sin modificar las existentes.
8. El sistema no valida la semántica del contexto (Feature 11).
9. Los disparadores basados en eventos del sistema que requieran entrega fiable entre componentes o procesos deben apoyarse en la capacidad de publicación duradera definida por EN-0208.
10. La generación automática de tareas a partir de eventos no debe depender de publicación directa no duradera cuando el flujo requiera garantías de reintento o recuperación tras fallo.

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Las automatizaciones se evalúan por calendario (A1–A4) o por eventos del sistema (A5).
- Cada evento de automatización debe generar una única tarea.
- Debe existir una clave de idempotencia (`automation_key`) asociada al evento.

---

## Dependencias

Esta feature puede depender de:

- F-0013
- EN-0208

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0005-idempotency-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- el sistema implementa la capacidad funcional descrita por esta feature
- los datos y entidades definidos por la feature pueden gestionarse de forma consistente con sus reglas del dominio
- el comportamiento observable de la feature respeta su alcance y fuera de alcance definidos
