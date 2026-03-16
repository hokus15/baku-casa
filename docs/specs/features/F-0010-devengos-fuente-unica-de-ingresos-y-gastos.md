# F-0010: Devengos (fuente única de ingresos y gastos)

---

## Objetivo

Registrar hechos económicos devengados (ingresos y gastos) asociados a propiedad y/o contrato, indicando quién es el obligado al pago (propietario o inquilino), de forma que esta entidad sea la fuente única para:

- Generación de facturas de renta, incluyendo IVA y retención cuando la operación los requiera.
- Registro de gastos de la propiedad.
- Cálculo de deuda del inquilino con el propietario.
- Preparar reporting fiscal futuro.

Todos los importes persistidos son siempre positivos o cero.  
Los devengos son inmutables.

---

## Alcance

Esta feature cubre el comportamiento funcional descrito en las secciones de datos, capacidades y reglas del dominio de esta especificación.

---

## Fuera de alcance

- No se definen exclusiones adicionales en la especificación original más allá de las restricciones ya descritas.

---

## Definiciones

- **Devengo**: hecho económico reconocido en una fecha con importe base, vencimiento y parámetros fiscales.
- **Devengo compensatorio**: devengo que revierte total otro devengo mediante `reversal_of_accrual_id`.
- **Parte obligada al pago (payer)**: `OWNER` o `TENANT`.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Devengo
- Devengo compensatorio

---

## Datos principales

La feature gestiona la siguiente información:

### Atribución económica/fiscal (derivada, no persistida)

El sistema NO persiste un campo explícito de “beneficiario” o “soportado por”.
La atribución se deriva de forma determinista:

- Para `type = INCOME`:
  - El ingreso se atribuye al propietario (OWNER) a efectos de reporting.
  - `payer` indica quién debe pagar (siempre TENANT).

- Para `type = EXPENSE`:
  - El gasto se atribuye a la propiedad/propietario (OWNER) como naturaleza del concepto.
  - Si `payer = TENANT`, el devengo representa un traslado contractual (el inquilino paga un gasto operativo), pero NO convierte ese gasto en deducible del propietario por defecto.

---

### Semántica contable mínima (invariante)

- `type = INCOME` significa: incremento de ingresos atribuibles al propietario (base_amount) por un servicio prestado (p.ej. alquiler).
- `type = EXPENSE` significa: gasto atribuible a la propiedad/propietario (base_amount) asociado a operación o mantenimiento.

- `payer` indica quién tiene la obligación de pago (quién debe pagar), no necesariamente quién recibe o soporta fiscalmente el concepto.

Restricción:
- Para `type = INCOME`, `payer` DEBE ser `TENANT`.
- Para `type = EXPENSE`, `payer` PUEDE ser `OWNER` o `TENANT` según responsabilidad contractual.

---

### Gastos con `payer = TENANT` (traslados)

- Un `Accrual` con `type = EXPENSE` y `payer = TENANT` representa un gasto operativo que:
  - existe a nivel de propiedad (conceptualmente),
  - pero cuya obligación de pago se traslada al inquilino por cláusula contractual.
- Estos devengos NO son gasto deducible del propietario en IRPF por defecto.
- Estos devengos SÍ impactan la deuda del contrato (porque el inquilino los debe pagar).
- Deben poder ordenarse de forma estable dentro de cada contrato para soportar la asignación posterior de pagos según la disciplina del sistema.

---

### Entidad

### Accrual

Esta entidad reutiliza la semántica económica común definida en:

- docs/specs/shared/SHARED-0004-financial-entity-semantics.md

### Campos obligatorios

- `property_id`
- `type`: enum { `INCOME`, `EXPENSE` }
- `payer`: enum { `OWNER`, `TENANT` }
- `accrual_date`
- `due_date`
- `base_amount` (decimal >= 0)
- `category`
- `idempotency_key`
- `sequence` (obligatorio si `payer = TENANT`)

`idempotency_key` reutiliza el contrato común definido en:

- docs/specs/shared/SHARED-0005-idempotency-contract.md

### Campos opcionales

- `contract_id`
- `service_period_start`
- `service_period_end`
- `description`
- `vat_rate_percent` (0–100)
- `withholding_rate_percent` (0–100)
- `source`
- `external_id`
- `reversal_of_accrual_id`

### Campos derivados (no persistidos)

- `vat_amount`
- `withholding_amount`
- `gross_amount`
- `net_payable_amount`
- `effect_sign`:
  - +1 si `reversal_of_accrual_id` es null
  - -1 si existe
- `effective_net_payable_amount = effect_sign * net_payable_amount`
- `applied_effective_amount` (por accrual y fecha de corte T):
    Sumatorio de importes efectivos aplicados a este devengo desde `PaymentApplication`,
    considerando el signo efectivo del Payment:
      `applied_effective_amount(T) = Σ (effect_sign(payment) * applied_amount)`
    para todas las aplicaciones con `payment_date <= T`.
- `outstanding_amount` (por accrual y fecha de corte T):
    `outstanding_amount(T) = effective_net_payable_amount - applied_effective_amount(T)`
    acotado inferiormente a 0 para efectos de “deuda pendiente”:
    `outstanding_debt_amount(T) = max(0, outstanding_amount(T))`

---

## Capacidades

El sistema debe permitir:

- Registrar devengos de ingreso y gasto asociados a propiedad y, cuando corresponda, a contrato.
- Registrar devengos compensatorios para corregir devengos previos sin modificar el historial.
- Consultar el estado económico derivado de cada devengo, incluyendo importes efectivos, importe aplicado y deuda pendiente.
- Garantizar creación segura ante reintentos mediante `idempotency_key`.

## Reglas del dominio

1. Un Accrual no puede modificarse ni eliminarse.
2. Cualquier corrección se realiza creando un Accrual compensatorio.
3. Un Accrual compensatorio debe:
   - Referenciar `reversal_of_accrual_id`
   - Pertenecer a la misma propiedad
   - Tener importes positivos
4. La suma algebraica de todos los devengos compensatorios asociados a un Accrual no puede exceder el `net_payable_amount` original del devengo revertido.
5. Si `payer = TENANT`, `contract_id` es obligatorio.
6. Si `payer = TENANT`, `sequence` es obligatorio y debe identificar un orden estable dentro del contrato.
7. `sequence`:
   - Es un entero incremental por contrato.
   - Es estrictamente creciente dentro de cada `contract_id`.
   - No se reutiliza ni se recalcula.
   - Su única finalidad es garantizar orden estable determinista para FIFO.
8. Los importes persistidos del `Accrual` siguen la disciplina común definida en docs/specs/shared/SHARED-0004-financial-entity-semantics.md
9. `vat_rate_percent` y `withholding_rate_percent` deben estar entre 0 y 100.
10. Los cálculos de saldo deben considerar importes efectivos conforme a la disciplina común definida en docs/specs/shared/SHARED-0004-financial-entity-semantics.md
11. Toda creación requiere `idempotency_key` y debe seguir el contrato común definido en docs/specs/shared/SHARED-0005-idempotency-contract.md
    Especialización local:
    - la identidad de idempotencia se evalúa dentro del ámbito declarado para operaciones de creación de devengos.
    - un mismo `idempotency_key` no puede producir más de un devengo materialmente distinto dentro de ese ámbito.
12. Restricción: `type = INCOME` ⇒ `payer = TENANT`.
13. Los saldos y deudas se calculan siempre usando importes efectivos:
   - Devengos: `effective_net_payable_amount`
   - Pagos: `effective_amount`
   - Aplicaciones: `effect_sign(payment) * applied_amount`
14. `outstanding_amount(T)` se define por devengo como:
   `effective_net_payable_amount - applied_effective_amount(T)`.
15. Para representar “deuda pendiente” (no negativa) se usa:
   `outstanding_debt_amount(T) = max(0, outstanding_amount(T))`.

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Reintento válido de creación con la misma identidad de idempotencia.
- Creación de gasto trasladado al inquilino con `payer = TENANT`.
- Reversión parcial o total de un devengo previo sin modificar el historial.

---

## Dependencias

Esta feature depende de:

- F-0009
- EN-0302

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

La lista anterior declara dependencias del item; este documento no sustituye la fuente estructural de dependencias.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0004-financial-entity-semantics.md
- docs/specs/shared/SHARED-0005-idempotency-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- el sistema implementa la capacidad funcional descrita por esta feature
- los datos y entidades definidos por la feature pueden gestionarse de forma consistente con sus reglas del dominio
- el comportamiento observable de la feature respeta su alcance y fuera de alcance definidos

---

