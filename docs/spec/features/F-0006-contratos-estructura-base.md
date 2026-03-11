# F-0006: Contratos (Estructura Base)

## Objetivo

Gestionar contratos de arrendamiento asociados a propiedades, definiendo su vigencia, inquilinos y condiciones económicas, garantizando consistencia temporal y dejando preparada la base para la futura generación de cargos y control de estados contractuales.

---

## Definiciones

- **Contrato**: acuerdo de arrendamiento vinculado a una única propiedad con un periodo de vigencia definido.
- **Inquilino**: persona física o jurídica arrendataria asociada al contrato.
- **Periodo de vigencia**: intervalo temporal comprendido entre fecha de inicio y fecha de fin contractual.
- **Extensión automática**: mecanismo configurable que prolonga el contrato tras su vencimiento inicial.
- **Estado del contrato**: condición derivada de fechas y reglas (no almacenado manualmente).
- **Día de cobro mensual**: día del mes en el que se devenga la renta.

---

## Entidad

### LeaseContract

**Campos obligatorios**

- `property_id`
- `start_date`
- `end_date`
- `dia_cobro_mes` (1–31)
- `tipo_pago_renta`: enum { Transferencia, Domiciliación, Efectivo, Otro }
- `sujeto_a_impuestos`: boolean (default: True)

**Campos opcionales**

- `deposito_importe`
- `reduccion_fiscal_porcentaje`
- `periodo_extension_automatica`
- `periodo_preaviso_finalizacion`

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

Los listados deben usar **paginacion obligatoria**.

Los parámetros de paginación configurables deben resolverse exclusivamente a través del configuration system definido en **EN-0202**.

No deben definirse mediante constantes hardcoded en adapters, servicios de aplicación o repositorios. Debe existir una única fuente de verdad para estos valores siguiendo la precedencia global de configuración:

`environment variables > config file > defaults`

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

## Reglas de negocio

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
7. `dia_cobro_mes` debe estar entre 1 y 31.
8. Si el día de cobro no existe en un mes determinado, se utilizará el último día válido anterior.
9. `reduccion_fiscal_porcentaje`, si existe, debe estar entre 0 y 100.
10. `deposito_importe`, si existe, debe ser positivo o cero.
11. `sujeto_a_impuestos` es True por defecto.
12. Si existe `periodo_extension_automatica`, el contrato puede prorrogarse automáticamente según dicha configuración.
13. `periodo_preaviso_finalizacion`, si existe, define el plazo mínimo previo a la finalización para evitar la prórroga automática.
14. Si existe `periodo_extension_automatica`, el contrato se prorroga automáticamente **incrementando `end_date`** en el **número de meses** indicado por `periodo_extension_automatica`.
  - La prórroga se aplica de forma **iterativa**: si tras extender `end_date` el contrato sigue vencido (respecto a la fecha de evaluación), se siguen aplicando extensiones sucesivas del mismo tamaño hasta que `end_date` quede en el futuro o en la fecha actual.
  - Si `periodo_extension_automatica` es **indefinido**, la prórroga se considera ilimitada (se permite el estado “en prórroga” sin un fin definitivo), manteniendo la lógica de preaviso.
  - La prórroga automática constituye una modificación explícita del contrato y debe registrarse mediante actualización auditable (updated_at, updated_by).
  - No debe sobrescribir la fecha original sin trazabilidad.
  
**Nota**: el estado del contrato se sigue derivando de `start_date`, `end_date` (prorrogada) y, si aplica, `periodo_preaviso_finalizacion`.
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
