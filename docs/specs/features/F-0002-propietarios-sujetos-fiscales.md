# F-0002: Propietarios (Sujetos fiscales)

---

## Objetivo

Gestionar propietarios como entidades fiscales independientes del operador autenticado, sirviendo como “master data” para futuras asociaciones con propiedades, contratos y reporting fiscal.

---

## Alcance

Esta feature cubre:

- Crear propietario
- Editar propietario
- Consultar detalle de propietario

---

## Fuera de alcance

- Relación propietario ↔ propiedad (se introduce en Feature 1).
- Validación avanzada del formato de tax_id/VAT por país.
- Multi-usuario y permisos por propietario.
- Cálculo de impuestos.
- Integraciones externas y canales de comunicación (por ejemplo, bots o mensajería), que deberán modelarse en features o módulos independientes referenciando `owner_id`.

---

## Definiciones

**Propietario (sujeto fiscal)**: persona o entidad titular fiscal (o potencial titular) de propiedades, usada para identificación, documentación y reporting.

- Un operador puede gestionar 0..N propietarios.
- No existen permisos por propietario (mono-usuario).

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Propietario (sujeto fiscal)
- Ver definiciones de dominio y datos principales de la feature

---

## Datos principales

La feature gestiona la siguiente información:

### Datos del propietario (mínimo viable)

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

### Auditoría y soft delete

Esta feature reutiliza el contrato común definido en:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md

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
- Los listados y búsquedas de propietarios deben seguir el contrato común definido en:
  docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Reglas del dominio

- `tax_id` debe identificar de forma única a cada propietario dentro del sistema.
- `entity_type` debe ser uno de los valores permitidos.
- `owner_id` debe ser estable e inmutable durante toda la vida del propietario.
- `email`, `land_line` y `mobile`, cuando existan, son datos informativos de contacto y no forman parte de la identidad del propietario.
- La semántica de auditoría y soft delete debe seguir:
  docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
- Las respuestas y errores expuestos por API deben seguir docs/specs/shared/SHARED-0003-api-response-conventions.md cuando aplique.
- No se requiere relación con propiedades en este MVP.

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Intento de alta de dos propietarios con el mismo `tax_id`.
- `entity_type` debe ser uno de los valores permitidos.
- `owner_id` debe ser estable e inmutable durante toda la vida del propietario.

---

## Dependencias

Esta feature puede depender de:

- F-0001

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
- docs/specs/shared/SHARED-0003-api-response-conventions.md
- docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- Crear propietario
- Editar propietario
- Consultar detalle de propietario

---

