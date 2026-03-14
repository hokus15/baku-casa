# F-0005: Gastos Recurrentes de la Propiedad (Master Data)

## Objetivo

Permitir definir en cada propiedad **plantillas de gastos recurrentes operativos**, que representen una configuración estructural para la futura generación automática de cargos.

Estas plantillas no generan movimientos económicos por sí mismas en esta feature, sino que establecen las reglas base para futuras automatizaciones.

---

## Definiciones

- **Plantilla de gasto recurrente**: configuración asociada a una propiedad que define un gasto operativo periódico estimado.
- **Categoría operativa**: valor perteneciente a una lista cerrada global de gastos recurrentes.
- **Periodicidad (rrule)**: regla de recurrencia que define la frecuencia del gasto.
- **Importe estimado**: valor orientativo utilizado como base para futuros cargos.
- **Fecha inicio**: fecha a partir de la cual la plantilla es válida.
- **Fecha fin**: fecha opcional que limita la vigencia de la plantilla.

---

## Entidad

### RecurringExpenseTemplate

**Campos obligatorios**

- `property_id`
- `category`: enum (lista cerrada global)
- `estimated_amount`: decimal positivo
- `periodicity`: rrule
- `start_date`: date

**Campos opcionales**

- `end_date`: date
- `notes`: string

### Auditoría

- `created_at`
- `created_by`
- `updated_at`
- `updated_by`
- `deleted_at` (nullable)
- `deleted_by` (nullable)

La eliminación es lógica y debe ser auditable.

**Lista cerrada de categorías**

- IBI
- Tasa residuos sólidos urbanos
- Comunidad
- Seguro
- Electricidad
- Agua
- Internet
- Telefonía
- Gas
- Alcantarillado
- Calefacción
- Suministros
- Limpieza
- Gestión
- Otros

**Relación**

- 1 Propiedad → 0..N RecurringExpenseTemplate

---

## Capacidades

- Crear plantilla de gasto recurrente para una propiedad.
- Editar plantilla.
- Eliminar plantilla (soft delete).
- Listar plantillas de una propiedad.
- Consultar detalle de una plantilla.
- Activar o desactivar implícitamente mediante rango de fechas.

---

Los listados deben usar **paginacion obligatoria**.

Los parámetros de paginación configurables deben resolverse exclusivamente a través del configuration system definido en **EN-0202**.

No deben definirse mediante constantes hardcoded en adapters, servicios de aplicación o repositorios. Debe existir una única fuente de verdad para estos valores siguiendo la precedencia global de configuración:

`environment variables > config file > defaults`

## Alcance

- Gestión CRUD de plantillas.
- Validación de categoría contra lista cerrada global.
- Validación estructural de `rrule`.
- Soporte de múltiples plantillas por propiedad.
- Permitir varias plantillas con misma categoría si difieren en rango temporal.

---

## Fuera de alcance

- Generación automática de cargos.
- Cálculo real de importes devengados.
- Integración con contratos o imputación a inquilinos.
- Ajustes automáticos por IPC u otras reglas.
- Contabilidad automática.

---

## Reglas de negocio

1. Una propiedad puede no tener ninguna plantilla de gasto recurrente.
2. Cada plantilla debe tener `category`, `estimated_amount`, `periodicity`, `start_date`.
3. `estimated_amount` debe ser positivo o cero.
4. `category` debe pertenecer a la lista cerrada global.
5. `end_date`, si existe, debe ser mayor o igual que `start_date`.
6. La vigencia de la plantilla está determinada por el rango `[start_date, end_date]`.
7. Se permiten múltiples plantillas con la misma categoría siempre que no exista solapamiento temporal inconsistente.
8. La eliminación debe ser lógica (soft delete).
9. El diseño debe permitir en el futuro generar cargos a partir de:
    - periodicidad (rrule)
    - importe estimado
    - rango de vigencia

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
