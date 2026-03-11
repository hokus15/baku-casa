# F-0009: Cláusulas de asignacion de gastos recurrentes de la propiedad

## Objetivo

Permitir que un contrato defina la reasignación de responsabilidad de uno o varios gastos recurrentes operativos de la propiedad al inquilino.

Estas cláusulas no crean nuevos gastos, sino que modifican quién asume económicamente los gastos ya definidos como plantillas en la propiedad.

---

## Definiciones

- **Gasto recurrente operativo**: plantilla de gasto definida a nivel de propiedad.
- **Cláusula de responsabilidad**: regla contractual que determina que el inquilino asume el pago de un gasto recurrente existente.
- **Reasignación de responsabilidad**: cambio del obligado al pago (propietario → inquilino), sin alterar la existencia del gasto.

---

## Entidad

### ExpenseResponsibilityClause

**Campos obligatorios**

- `contract_id`
- `property_recurring_expense_template_id`

**Campos opcionales**

- `start_date`
- `end_date`
- `notes`

### Auditoría

- `created_at`
- `created_by`
- `updated_at`
- `updated_by`
- `deleted_at` (nullable)
- `deleted_by` (nullable)

La eliminación es lógica y auditable.

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

Los listados deben usar **paginacion obligatoria**.

Los parámetros de paginación configurables deben resolverse exclusivamente a través del configuration system definido en **EN-0202**.

No deben definirse mediante constantes hardcoded en adapters, servicios de aplicación o repositorios. Debe existir una única fuente de verdad para estos valores siguiendo la precedencia global de configuración:

`environment variables > config file > defaults`

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

## Reglas de negocio

1. Un contrato puede tener 0..N cláusulas de responsabilidad.
2. Solo pueden referenciarse gastos recurrentes existentes en la propiedad.
3. La cláusula no crea un nuevo gasto; solo reasigna la responsabilidad.
4. Un mismo gasto recurrente no puede estar duplicado en cláusulas activas para el mismo contrato con rangos solapados.
5. Si se define `start_date` y `end_date`, deben respetar coherencia temporal (`end_date ≥ start_date`).
6. La responsabilidad efectiva en una fecha se determina evaluando:
   - vigencia del contrato
   - vigencia de la plantilla de gasto
   - vigencia de la cláusula
7. La eliminación debe ser lógica (soft delete).
8. En ausencia de cláusula activa, el gasto se considera responsabilidad del propietario.
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
