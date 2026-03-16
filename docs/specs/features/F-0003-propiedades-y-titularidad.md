# F-0003: Propiedades y Titularidad

---

## Objetivo

Permitir registrar propiedades y vincularlas a uno o varios propietarios (sujetos fiscales), estableciendo la titularidad actual sin histórico.

Este slice habilita la base estructural para contratos, contabilidad y fiscalidad.

---

## Alcance

Esta feature cubre:

- Crear propiedad
- Editar propiedad
- Consultar detalle de propiedad

---

## Fuera de alcance

- Operación de adquisición y venta.
- Gastos recurrentes.
- Amortizaciones fiscales.
- Contratos.
- Contabilidad.
- Facturación.

---

## Definiciones

**Propiedad**: unidad inmobiliaria gestionable.

**Titularidad**: relación entre Propiedad y Propietario con porcentaje de participación.

- Una propiedad tiene 1..N propietarios.
- Un propietario puede tener 0..N propiedades.
- No se guarda histórico de cambios de titularidad (solo estado actual).

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Propiedad
- Titularidad

---

## Datos principales

La feature gestiona la siguiente información:

### Datos de la propiedad

- `property_id`
- `name`
- `type` (lista cerrada):
  - Vivienda
  - Apartamento
  - Plaza de aparcamiento
  - Estudio
  - Local comercial
  - Oficina
  - Trastero
  - Otro
- `description` (opcional)
- `address` (opcional)
- `city` (opcional)
- `postal_code` (opcional)
- `province` (opcional)
- `country` (opcional)
- `cadastral_reference` (opcional)
- `cadastral_value` (opcional)
- `cadastral_land_value` (opcional)
- `cadastral_construction_value` (calculado = valor_catastral − valor_catastral_suelo) (opcional)
- `construction_ratio` (calculado = valor_catastral_construccion / valor_catastral) (opcional)
- Invariante del calculo catastral: `cadastral_construction_value = cadastral_value - cadastral_land_value`.
- `cadastral_land_value` no puede ser mayor que `cadastral_value`.
- `cadastral_construction_value` no puede ser negativo.
- `cadastral_value_revised` (boolean) (opcional)
- `acquisition_date` (opcional)
- `acquisition_type` (opcional) (lista cerrada) Tipo de adquisición para el informe de IRPF:
  - Onerosa
  - Lucrativa
  - Ambas
- `transfer_date` (opcional)
- `transfer_type` (opcional) (lista cerrada) Tipo de transmision para el informe de IRPF:
  - Onerosa
  - Lucrativa
  - Ambas
- `fiscal_nature` (opcional) (lista cerrada):
  - Urbana
  - Rústica
- `fiscal_situation` (opcional) (lista cerrada):
  - Con referencia catastral
  - Situado en el Pais Vasco
  - Situado en Navarra
  - Sin referencia catastral

### Auditoría y soft delete

Esta feature reutiliza el contrato común definido en:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md

---

### Titularidad

La relación Propiedad ↔ Propietario incluye:

- `owner_id`
- `property_id`
- `ownership_percentage`

`ownership_percentage` admite hasta 2 decimales.

Solo puede existir una titularidad activa por cada par (`property_id`, `owner_id`).

Si una **propiedad es eliminada mediante soft-delete**, las relaciones de titularidad asociadas **no se eliminan físicamente**, pero se debe aplicar sobre ellas un **soft-delete en cascada**, utilizando sus propios campos de auditoría de borrado, y no deben aparecer en consultas normales de propiedades o titularidades activas.

---

## Capacidades

El sistema debe permitir:

- Crear propiedad
- Editar propiedad
- Consultar detalle de propiedad
- Listar propiedades
- Asignar propietarios a una propiedad
- Modificar porcentajes de titularidad
- Consultar propiedades de un propietario
- Consultar propietarios de una propiedad
- Eliminar propiedad (soft-delete)
- Los listados y consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Reglas del dominio

- Una propiedad debe tener al menos un propietario.
- `type` debe ser uno de los valores permitidos.
- `cadastral_construction_value` y `construction_ratio` son campos derivados y no editables directamente.
- Los importes monetarios de esta feature no pueden ser negativos.
- Si se informan `cadastral_value` y `cadastral_land_value`, debe cumplirse `cadastral_land_value <= cadastral_value`.
- La suma permitida de `ownership_percentage` es 100.
- Se acepta una suma total de `ownership_percentage` menor que 100.
- Se rechaza una suma total de `ownership_percentage` mayor que 100.

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Una propiedad debe tener al menos un propietario.
- `type` debe ser uno de los valores permitidos.
- `cadastral_construction_value` y `construction_ratio` son campos derivados y no editables directamente.

---

## Dependencias

Esta feature puede depender de:

- F-0002

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

- Crear propiedad
- Editar propiedad
- Consultar detalle de propiedad

---


