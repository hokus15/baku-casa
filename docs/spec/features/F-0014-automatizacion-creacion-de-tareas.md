# F-0014: Automatización: Creación de Tareas

## Objetivo

Generar automáticamente tareas (Feature 11) a partir del master data del sistema (rentas, gastos recurrentes, cláusulas de actualización de renta, preavisos) y de eventos del sistema (p.ej. creación de devengos facturables), para supervisión previa a la creación de devengos u otras entidades.

El sistema no ejecuta acciones automáticamente. La ejecución depende del cliente que consume la tarea.

---

## Definiciones

- **Automatización**: regla que genera tareas cuando se cumple una condición temporal o un evento del sistema.
- **Evento de automatización**: combinación única de:
  - tipo de automatización
  - entidad origen
  - periodo u ocurrencia concreta
- **Idempotencia**: garantía de que un mismo evento de automatización genera una única tarea.

---

## Tipos de tarea (task_type)

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

## Disparadores de automatización

### A1 — Renta mensual

Se genera una tarea cuando se cumple el día de cobro del contrato.

Regla de fecha:
- `dia_cobro_mes`
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
  - `tipo_actualizacion`
  - parámetros de la cláusula

---

### A4 — Preaviso contractual

Se genera una tarea cuando se cumple la fecha:

`effective_end_date - periodo_preaviso_finalizacion`

Considerando prórrogas automáticas.

Contexto mínimo:
- `contract_id`
- `effective_end_date`
- `periodo_preaviso_finalizacion`

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

---

## Reglas de negocio

1. Las automatizaciones se evalúan por calendario (A1–A4) o por eventos del sistema (A5).
2. Cada evento de automatización debe generar una única tarea.
3. Debe existir una clave de idempotencia (`automation_key`) asociada al evento.
4. Las tareas automáticas deben incluir en su contexto toda la información necesaria para ejecutar la acción.
5. La creación de una tarea no implica ejecución automática.
6. La ejecución debe ser segura ante reintentos (no crear duplicados).
7. El sistema debe permitir añadir nuevas automatizaciones sin modificar las existentes.
8. El sistema no valida la semántica del contexto (Feature 11).

---

## Fuera de alcance

- Motor de workflows.
- Ejecución automática sin supervisión.
- Notificaciones externas.
- Cálculo automático de índices oficiales.

---

---

## Dependencias y trazabilidad

### Depende de
- F-0011

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

### Condicionales
- ADR-0010 (si esta feature publica/consume eventos con entrega duradera)


---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Correlacion por request mediante `correlation_id`.
