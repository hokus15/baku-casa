# F-0003: Propiedades y Titularidad

## Objetivo

Permitir registrar propiedades y vincularlas a uno o varios propietarios (sujetos fiscales), estableciendo la titularidad actual sin histórico.

Este slice habilita la base estructural para contratos, contabilidad y fiscalidad.

---

## Definiciones

**Propiedad**: unidad inmobiliaria gestionable.

**Titularidad**: relación entre Propiedad y Propietario con porcentaje de participación.

- Una propiedad tiene 1..N propietarios.
- Un propietario puede tener 0..N propiedades.
- No se guarda histórico de cambios de titularidad (solo estado actual).

---

## Datos de la propiedad

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

### Metadatos de auditoría

Todas las entidades creadas por esta feature deben incluir los siguientes campos de auditoría:

- `created_at`
- `created_by`
- `updated_at`
- `updated_by`
- `deleted_at`
- `deleted_by`

La eliminación de propiedades debe implementarse mediante **soft-delete**, utilizando `deleted_at` y `deleted_by`.

La eliminación de titularidades debe implementarse mediante **soft-delete**, utilizando `deleted_at` y `deleted_by`.

---

## Titularidad

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

Los listados deben usar **paginacion obligatoria** con `page=1` y `page_size=20` como valores por defecto.

`max_page_size=100` es el limite maximo por defecto, y tanto `page_size` como `max_page_size` deben ser configurables de forma transversal para todas las listas.

Los parámetros de paginación configurables deben resolverse exclusivamente a través del configuration system definido en **EN-0202**.

No deben definirse mediante constantes hardcoded en adapters, servicios de aplicación o repositorios. Debe existir una única fuente de verdad para estos valores siguiendo la precedencia global de configuración:

`environment variables > config file > defaults`

---

## Reglas de negocio

- Una propiedad debe tener al menos un propietario.
- `type` debe ser uno de los valores permitidos.
- `cadastral_construction_value` y `construction_ratio` son campos derivados y no editables directamente.
- Los importes monetarios de esta feature no pueden ser negativos.
- Si se informan `cadastral_value` y `cadastral_land_value`, debe cumplirse `cadastral_land_value <= cadastral_value`.
- La suma permitida de `ownership_percentage` es 100.
- Se acepta una suma total de `ownership_percentage` menor que 100.
- Se rechaza una suma total de `ownership_percentage` mayor que 100.

---

## Fuera de alcance (en este slice)

- Operación de adquisición y venta.
- Gastos recurrentes.
- Amortizaciones fiscales.
- Contratos.
- Contabilidad.
- Facturación.

---

## Dependencias y trazabilidad

### Depende de
- F-0002

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
- ADR-0013
- ADR-0014


---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Correlacion por request mediante `correlation_id`.

---

## Reglas de serialización API

- En las respuestas de la API no deben incluirse campos con valor `null`.
- Los `timestamps` deben serializarse en formato ISO-8601 UTC con sufijo `Z`.
- Las fechas puras deben serializarse en formato `YYYY-MM-DD`.
