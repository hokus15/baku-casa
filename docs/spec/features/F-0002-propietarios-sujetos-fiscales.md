# F-0002: Propietarios (Sujetos fiscales)

## Objetivo

Gestionar propietarios como entidades fiscales independientes del operador autenticado, sirviendo como “master data” para futuras asociaciones con propiedades, contratos y reporting fiscal.

---

## Definiciones

**Propietario (sujeto fiscal)**: persona o entidad titular fiscal (o potencial titular) de propiedades, usada para identificación, documentación y reporting.

- Un operador puede gestionar 0..N propietarios.
- No existen permisos por propietario (mono-usuario).

---

## Datos del propietario (mínimo viable)

### Identidad

- `owner_id`
- `entity_type` (lista cerrada):
  - PERSONA_FISICA
  - PERSONA_JURIDICA
  - ESPJ
- `first_name`
- `last_name`
- `legal_name`
- `tax_id` (identificador fiscal)
- `stamp_image` (opcional; imagen en formato base64 con mime_type ejemplo: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...)

---

### Domicilio fiscal

- `fiscal_address_line1`
- `fiscal_address_city`
- `fiscal_address_postal_code`
- `fiscal_address_country` (default ES)

---

### Contacto (opcional)

- `email` (opcional)
- `land_line` (opcional)
- `land_line_country_code` (default 34 -> España)
- `mobile` (opcional)
- `mobile_country_code` (default 34 -> España)


---


### Metadatos

- `created_at`
- `created_by`
- `updated_at`
- `updated_by`
- `deleted_at`
- `deleted_by`

---

## Capacidades

El sistema debe permitir:

- Crear propietario
- Editar propietario
- Consultar detalle de propietario
- Listar propietarios
- Buscar propietarios por `tax_id` y/o `legal_name`
- Eliminar propietario mediante **soft delete** (estableciendo `deleted_at`)
- Consultar detalle y listado con `include_deleted` opcional (default `false`)

Los listados y busquedas de propietarios deben usar paginacion obligatoria.

Los valores por defecto y limites maximos de paginacion deben ser configurables de forma transversal y resolverse exclusivamente mediante el configuration system definido en EN-0202, con precedencia global:

`environment variables > config file > defaults`.

No deben definirse valores hardcoded de paginacion fuera de la fuente central de configuracion.

---

## Reglas de negocio

- `tax_id` debe ser único por propietario, usando normalizacion previa con `trim`, conversion a mayusculas, eliminacion de espacios y eliminacion de guiones antes de validar y persistir.
- `entity_type` debe ser uno de los valores permitidos.
- `owner_id` debe ser estable e inmutable durante toda la vida del propietario.
- `email`, `land_line` y `mobile`, cuando existan, son datos informativos de contacto y no forman parte de la identidad del propietario.
- `created_by` y `updated_by` son obligatorios y deben exponerse en la API.
- `deleted_by` debe registrarse en el soft delete y exponerse en la API cuando corresponda.
- Los propietarios eliminados mediante `deleted_at` no deben aparecer en listados ni búsquedas por defecto.
- Los campos con valor `null` NO deben exponerse en la API.
- Tanto el listado como el detalle de propietario deben permitir opcionalmente incluir propietarios eliminados mediante `deleted_at` usando `include_deleted = true`.
- Las descripciones de errores y la documentacion de la API deben estar en español, aunque los codigos de error y los nombres tecnicos de campos permanezcan en ingles.
- No se requiere relación con propiedades en este MVP.

---

## Fuera de alcance

- Relación propietario ↔ propiedad (se introduce en Feature 1).
- Validación avanzada del formato de tax_id/VAT por país.
- Multi-usuario y permisos por propietario.
- Cálculo de impuestos.
- Integraciones externas y canales de comunicación (por ejemplo, bots o mensajería), que deberán modelarse en features o módulos independientes referenciando `owner_id`.

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

---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Exclusion de PII de propietarios en logs (`tax_id`, `legal_name`, `email`, `land_line`, `mobile`, campos de direccion fiscal); usar solo identificadores tecnicos y de auditoria seguros como `owner_id` y `correlation_id`.
- Correlacion por request mediante `correlation_id`.
