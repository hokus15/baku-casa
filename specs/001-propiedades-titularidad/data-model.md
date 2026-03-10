# Data Model - F-0003 Propiedades y Titularidad

## Entidades

## 1) Property

- Description: Unidad inmobiliaria gestionable del sistema.
- Fields:
  - `property_id` (ID opaco, inmutable, unico)
  - `name` (requerido)
  - `type` (enum cerrado requerido: `VIVIENDA`, `APARTAMENTO`, `PLAZA_APARCAMIENTO`, `ESTUDIO`, `LOCAL_COMERCIAL`, `OFICINA`, `TRASTERO`, `OTRO`)
  - `description` (opcional)
  - `address` (opcional)
  - `city` (opcional)
  - `postal_code` (opcional)
  - `province` (opcional)
  - `country` (opcional)
  - `cadastral_reference` (opcional)
  - `cadastral_value` (opcional, Decimal >= 0)
  - `cadastral_land_value` (opcional, Decimal >= 0)
  - `cadastral_construction_value` (derivado, no editable)
  - `construction_ratio` (derivado, no editable; porcentaje 0-100 cuando aplica)
  - `cadastral_value_revised` (opcional, boolean)
  - `acquisition_date` (opcional, `YYYY-MM-DD`)
  - `acquisition_type` (opcional, enum: `ONEROSA`, `LUCRATIVA`, `AMBAS`)
  - `transfer_date` (opcional, `YYYY-MM-DD`)
  - `transfer_type` (opcional, enum: `ONEROSA`, `LUCRATIVA`, `AMBAS`)
  - `fiscal_nature` (opcional, enum: `URBANA`, `RUSTICA`)
  - `fiscal_situation` (opcional, enum: `CON_REFERENCIA_CATASTRAL`, `PAIS_VASCO`, `NAVARRA`, `SIN_REFERENCIA_CATASTRAL`)
  - `created_at` (UTC, ISO-8601 `Z`)
  - `created_by` (requerido)
  - `updated_at` (UTC, ISO-8601 `Z`)
  - `updated_by` (requerido)
  - `deleted_at` (UTC, ISO-8601 `Z`, nullable)
  - `deleted_by` (nullable; requerido cuando `deleted_at` existe)
- Validation rules:
  - `name` obligatorio y no vacio.
  - `type` solo valores del enum cerrado.
  - `cadastral_construction_value = cadastral_value - cadastral_land_value` cuando ambos valores existen.
  - `construction_ratio = (cadastral_construction_value / cadastral_value) * 100` cuando aplica; si `cadastral_value` es 0 o ausente, no aplica.
  - Campos derivados no se aceptan como editables en input.

## 2) Ownership

- Description: Relacion de titularidad vigente entre propiedad y propietario.
- Fields:
  - `property_id` (FK a Property)
  - `owner_id` (FK referencial a Owner de F-0002)
  - `ownership_percentage` (Decimal, rango 0-100, maximo 2 decimales)
  - `created_at` (UTC, ISO-8601 `Z`)
  - `created_by` (requerido)
  - `updated_at` (UTC, ISO-8601 `Z`)
  - `updated_by` (requerido)
  - `deleted_at` (UTC, ISO-8601 `Z`, nullable)
  - `deleted_by` (nullable; requerido cuando `deleted_at` existe)
- Validation rules:
  - Existe como maximo una titularidad activa por (`property_id`, `owner_id`).
  - `ownership_percentage` debe estar en rango 0-100 y con precision maxima de 2 decimales.
  - Para una propiedad activa, la suma de titularidades activas:
    - puede ser menor que 100
    - no puede ser mayor que 100
  - Toda propiedad activa debe tener al menos una titularidad activa.

## 3) OwnerReference (from F-0002)

- Description: Referencia a propietario fiscal existente.
- Fields relevantes:
  - `owner_id` (ID opaco existente)
  - estado activo/inactivo para validar asociacion funcional
- Validation rules:
  - No se permite crear titularidad con `owner_id` inexistente.

## Relaciones

- `Property` 1 --- N `Ownership` (activas e historicas por soft-delete)
- `OwnerReference` 1 --- N `Ownership`
- Relacion efectiva `Property` <-> `OwnerReference` es N --- N via `Ownership`.

## Estados y transiciones

1. Property activa
  - `deleted_at = null`
  - visible en consultas activas.

2. Property eliminada logicamente
  - `deleted_at != null`
  - no visible en consultas activas.
  - dispara soft-delete en cascada de titularidades activas asociadas.

3. Ownership activa
  - `deleted_at = null`
  - computa para reglas de suma y consultas activas.

4. Ownership eliminada logicamente
  - `deleted_at != null`
  - no participa en suma activa ni en consultas activas.

## Invariantes

- Timestamps en UTC con serializacion ISO-8601 `Z`.
- Campos de fecha pura en `YYYY-MM-DD`.
- Porcentajes en escala 0-100 (sin representacion 0-1 en dominio ni contrato).
- Soft-delete permitido por tratarse de master data no economica.
- No se introducen entidades ni eventos de ledger.
