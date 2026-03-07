# F-0010: Devengos (fuente única de ingresos y gastos)

## Objetivo

Registrar hechos económicos devengados (ingresos y gastos) asociados a propiedad y/o contrato, indicando quién es el obligado al pago (propietario o inquilino), de forma que esta entidad sea la fuente única para:

- Generación de facturas de renta (con IVA y retención cuando aplique).
- Registro de gastos de la propiedad.
- Cálculo de deuda del inquilino con el propietario.
- Preparar reporting fiscal futuro.

Todos los importes persistidos son siempre positivos o cero.  
Los devengos son inmutables.

---

## Definiciones

- **Devengo**: hecho económico reconocido en una fecha con importe base, vencimiento y parámetros fiscales.
- **Devengo compensatorio**: devengo que revierte total otro devengo mediante `reversal_of_accrual_id`.
- **Base imponible (`base_amount`)**: importe principal del devengo, sin IVA añadido.
- **IVA (`vat_amount`)**: importe calculado a partir de `base_amount` y `vat_rate_percent`.
- **Retención (`withholding_amount`)**: importe calculado a partir de `base_amount` y `withholding_rate_percent`.
- **Importe bruto (`gross_amount`)**: `base_amount + vat_amount`.
- **Importe neto exigible (`net_payable_amount`)**: `gross_amount - withholding_amount`.
- **Parte obligada al pago (payer)**: `OWNER` o `TENANT`.

---

## Atribución económica/fiscal (derivada, no persistida)

El sistema NO persiste un campo explícito de “beneficiario” o “soportado por”.
La atribución se deriva de forma determinista:

- Para `type = INCOME`:
  - El ingreso se atribuye al propietario (OWNER) a efectos de reporting.
  - `payer` indica quién debe pagar (siempre TENANT).

- Para `type = EXPENSE`:
  - El gasto se atribuye a la propiedad/propietario (OWNER) como naturaleza del concepto.
  - Si `payer = TENANT`, el devengo representa un traslado contractual (el inquilino paga un gasto operativo), pero NO convierte ese gasto en deducible del propietario por defecto.

---

## Semántica contable mínima (invariante)

- `type = INCOME` significa: incremento de ingresos atribuibles al propietario (base_amount) por un servicio prestado (p.ej. alquiler).
- `type = EXPENSE` significa: gasto atribuible a la propiedad/propietario (base_amount) asociado a operación o mantenimiento.

- `payer` indica quién tiene la obligación de pago (quién debe pagar), no necesariamente quién recibe o soporta fiscalmente el concepto.

Restricción:
- Para `type = INCOME`, `payer` DEBE ser `TENANT`.
- Para `type = EXPENSE`, `payer` PUEDE ser `OWNER` o `TENANT` según responsabilidad contractual.

---

## Gastos con `payer = TENANT` (traslados)

- Un `Accrual` con `type = EXPENSE` y `payer = TENANT` representa un gasto operativo que:
  - existe a nivel de propiedad (conceptualmente),
  - pero cuya obligación de pago se traslada al inquilino por cláusula contractual.
- Estos devengos NO son gasto deducible del propietario en IRPF por defecto.
- Estos devengos SÍ impactan la deuda del contrato (porque el inquilino los debe pagar).
- Debe existir restricción única (contract_id, sequence).
- La generación de sequence debe estar protegida frente a concurrencia.

---

## Entidad

### Accrual

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

## Reglas de negocio

1. Un Accrual no puede modificarse ni eliminarse.
2. Cualquier corrección se realiza creando un Accrual compensatorio.
3. Un Accrual compensatorio debe:
   - Referenciar `reversal_of_accrual_id`
   - Pertenecer a la misma propiedad
   - Tener importes positivos
4. La suma algebraica de todos los devengos compensatorios asociados a un Accrual no puede exceder el `net_payable_amount` original del devengo revertido.
5. Si `payer = TENANT`, `contract_id` es obligatorio.
6. Si `payer = TENANT`, `sequence` es obligatorio y único por contrato.
7. `sequence`:
   - Es un entero incremental por contrato.
   - Se genera en el momento de creación del Accrual.
   - Es estrictamente creciente dentro de cada `contract_id`.
   - No se reutiliza ni se recalcula.
   - Su única finalidad es garantizar orden estable determinista para FIFO.
8. Los importes persistidos son siempre positivos o cero.
9. `vat_rate_percent` y `withholding_rate_percent` deben estar entre 0 y 100.
10. Los cálculos de saldo deben considerar importes efectivos (con `effect_sign`).
11. Toda creación requiere `idempotency_key`.
	Idempotency scope:
	- `idempotency_key` es única por tipo de entidad económica.
	- El par (`entity_type`, `idempotency_key`) debe ser único globalmente.
	- Si se recibe una petición repetida con la misma clave:
		- Se devuelve el resultado previamente creado.
		- No se crean efectos adicionales.
	- Si la misma clave se usa con parámetros distintos:
		- El sistema debe rechazar la operación.
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

---

## Dependencias y trazabilidad

### Depende de
- (ninguna explícita)

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
