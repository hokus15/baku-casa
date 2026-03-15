# F-0005: Gastos Recurrentes de la Propiedad (Master Data)

---

## Objetivo

Permitir definir en cada propiedad **plantillas de gastos recurrentes operativos**, que representen una configuración estructural para la futura generación automática de cargos.

Estas plantillas no generan movimientos económicos por sí mismas en esta feature, sino que establecen las reglas base para futuras automatizaciones.

---

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

## Definiciones

- **Plantilla de gasto recurrente**: configuración asociada a una propiedad que define un gasto operativo periódico estimado.
- **Categoría operativa**: valor perteneciente a una lista cerrada global de gastos recurrentes.
- **Periodicidad (rrule)**: regla de recurrencia que define la frecuencia del gasto.
- **Importe estimado**: valor orientativo utilizado como base para futuros cargos.
- **Fecha inicio**: fecha a partir de la cual la plantilla es válida.
- **Fecha fin**: fecha opcional que limita la vigencia de la plantilla.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Plantilla de gasto recurrente
- Categoría operativa

---

## Datos principales

La feature gestiona la siguiente información:

### Entidad

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

### Auditoría y soft delete

Esta feature reutiliza el contrato común definido en:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md

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

Los listados y consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md.

---

## Reglas del dominio

1. Una propiedad puede no tener ninguna plantilla de gasto recurrente.
2. Cada plantilla debe tener `category`, `estimated_amount`, `periodicity`, `start_date`.
3. `estimated_amount` debe ser positivo o cero.
4. `category` debe pertenecer a la lista cerrada global.
5. `end_date`, si existe, debe ser mayor o igual que `start_date`.
6. La vigencia de la plantilla está determinada por el rango `[start_date, end_date]`.
7. Se permiten múltiples plantillas con la misma categoría siempre que no exista solapamiento temporal inconsistente.
8. La eliminación debe seguir la semántica compartida de soft delete definida en docs/specs/shared/SHARED-0001-audit-and-soft-delete.md.
9. El diseño debe permitir en el futuro generar cargos a partir de:
    - periodicidad (rrule)
    - importe estimado
    - rango de vigencia

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Una propiedad puede no tener ninguna plantilla de gasto recurrente.
- Cada plantilla debe tener `category`, `estimated_amount`, `periodicity`, `start_date`.
- `estimated_amount` debe ser positivo o cero.

---

## Dependencias

Esta feature puede depender de:

- F-0003

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

- Crear plantilla de gasto recurrente para una propiedad.
- Editar plantilla.
- Eliminar plantilla (soft delete).

---

