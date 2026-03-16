# F-0006: Contratos (Estructura Base)

---

## Objetivo

Gestionar contratos de arrendamiento asociados a propiedades, definiendo su vigencia, inquilinos y condiciones económicas, garantizando consistencia temporal y dejando preparada la base para la futura generación de cargos y control de estados contractuales.

---

## Alcance

- Gestión completa de contratos.
- Validación de integridad temporal.
- Soporte de múltiples contratos históricos por propiedad.
- Soporte de múltiples inquilinos por contrato.
- Configuración de extensión automática.
- Definición de condiciones económicas básicas.

---

## Fuera de alcance

- Generación automática de rentas.
- Gestión de pagos reales.
- Reparto porcentual entre inquilinos.
- Histórico de cambios de inquilinos.
- Cálculo fiscal automático.
- Penalizaciones por impago.

---

## Definiciones

- **Contrato**: acuerdo de arrendamiento vinculado a una única propiedad con un periodo de vigencia definido.
- **Inquilino**: persona física o jurídica arrendataria asociada al contrato.
- **Periodo de vigencia**: intervalo temporal comprendido entre fecha de inicio y fecha de fin contractual.
- **Extensión automática**: mecanismo configurable que prolonga el contrato tras su vencimiento inicial.
- **Estado del contrato**: condición derivada de fechas y reglas (no almacenado manualmente).
- **Día de cobro mensual**: día del mes en el que se devenga la renta.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Contrato
- Inquilino

---

## Datos principales

La feature gestiona la siguiente información:

### Entidad

### LeaseContract

**Campos obligatorios**

- `property_id`
- `start_date`
- `end_date`
- `charge_day_of_month` (1–31)
- `rent_payment_method`: enum { Transfer, DirectDebit, Cash, Other }
- `is_taxable`: boolean (default: True)

**Campos opcionales**

- `deposit_amount`
- `tax_reduction_percent`
- `auto_extension_period`
- `termination_notice_period`

**Relaciones**

- 1 Propiedad → 0..N LeaseContract
- 1 LeaseContract → 1..N Inquilino

---

### Tenant

**Campos mínimos**

- `name`
- `identification`
- `contact_info` (opcional)

No se gestionan porcentajes de participación ni histórico de cambios dentro del contrato.

---

## Capacidades

- Crear contrato asociado a una propiedad.
- Editar contrato.
- Eliminar contrato (según reglas de dominio).
- Asociar uno o múltiples inquilinos a un contrato.
- Consultar contratos de una propiedad.
- Derivar estado del contrato en base a fechas y reglas.
- Validar no solapamiento temporal.

---

Los listados y consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Reglas del dominio

1. Un contrato pertenece a exactamente una propiedad.
2. Una propiedad puede tener 0..N contratos.
3. No puede existir solapamiento de periodos de vigencia entre contratos de una misma propiedad.
4. Un contrato debe tener al menos un inquilino.
5. No se gestionan porcentajes entre inquilinos.
6. El estado del contrato se deriva de:
   - fecha actual
   - start_date
   - end_date
   - reglas de extensión automática
7. `charge_day_of_month` debe estar entre 1 y 31.
8. Si el día de cobro no existe en un mes determinado, se utilizará el último día válido anterior.
9. `tax_reduction_percent`, si existe, debe estar entre 0 y 100.
10. `deposit_amount`, si existe, debe ser positivo o cero.
11. `is_taxable` es True por defecto.
12. Si existe `auto_extension_period`, el contrato puede prorrogarse automáticamente según dicha configuración.
13. `termination_notice_period`, si existe, define el plazo mínimo previo a la finalización para evitar la prórroga automática.
14. Si existe `auto_extension_period`, el contrato se prorroga automáticamente **incrementando `end_date`** en el **número de meses** indicado por `auto_extension_period`.
  - La prórroga se aplica de forma **iterativa**: si tras extender `end_date` el contrato sigue vencido (respecto a la fecha de evaluación), se siguen aplicando extensiones sucesivas del mismo tamaño hasta que `end_date` quede en el futuro o en la fecha actual.
  - Si `auto_extension_period` es **indefinido**, la prórroga se considera ilimitada (se permite el estado “en prórroga” sin un fin definitivo), manteniendo la lógica de preaviso.
  - La prórroga automática constituye una modificación explícita del contrato y debe registrarse según el contrato común de auditoría definido en docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
  - No debe sobrescribir la fecha original sin trazabilidad.
  
**Nota**: el estado del contrato se sigue derivando de `start_date`, `end_date` (prorrogada) y, si aplica, `termination_notice_period`.
---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Un contrato pertenece a exactamente una propiedad.
- Una propiedad puede tener 0..N contratos.
- No puede existir solapamiento de periodos de vigencia entre contratos de una misma propiedad.

---

## Dependencias

Esta feature depende de:

- F-0002
- F-0003

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

La lista anterior declara dependencias del item; este documento no sustituye la fuente estructural de dependencias.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
- docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- Crear contrato asociado a una propiedad.
- Editar contrato.
- Eliminar contrato (según reglas de dominio).

---

