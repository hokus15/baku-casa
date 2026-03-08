# Data Model - F-0002 Propietarios (Sujetos Fiscales)

## Entities

## 1) Owner

- Description: Fiscal subject managed by the authenticated operator as master data.
- Canonical fields (English names for code/persistence):
  - `owner_id` (opaque, unique, immutable)
  - `entity_type` (enum: `PERSONA_FISICA`, `PERSONA_JURIDICA`, `ESPJ`)
  - `first_name` (required)
  - `last_name` (required)
  - `legal_name` (required)
  - `tax_id` (required, unique among active owners using normalized value)
  - `stamp_image` (optional; image payload in base64 with mime prefix)
  - `fiscal_address_line1` (required)
  - `fiscal_address_city` (required)
  - `fiscal_address_postal_code` (required)
  - `fiscal_address_country` (required, default `ES`)
  - `email` (optional, informational contact field)
  - `land_line` (optional, informational contact field)
  - `land_line_country_code` (optional, default `34`)
  - `mobile` (optional, informational contact field)
  - `mobile_country_code` (optional, default `34`)
  - `created_at` (UTC, required)
  - `created_by` (required)
  - `updated_at` (UTC, required)
  - `updated_by` (required)
  - `deleted_at` (UTC, nullable)
  - `deleted_by` (nullable; required when `deleted_at` is set)
- Validation rules:
  - `entity_type` must belong to closed enum.
  - `owner_id` cannot be changed after creation.
  - `tax_id` normalization pipeline: trim -> uppercase -> remove spaces -> remove hyphens.
  - Uniqueness for `tax_id` is enforced on normalized value among active records only (`deleted_at` is null).
  - `stamp_image` is optional and can be absent.
  - Empty `email`, `land_line`, and `mobile` are treated as absent.
  - `email` is optional and is not part of owner identity or uniqueness.

## Persistence projection (English naming)

- Table: `owners`
- Columns:
  - `owner_id`
  - `entity_type`
  - `first_name`
  - `last_name`
  - `legal_name`
  - `tax_id`
  - `stamp_image`
  - `fiscal_address_line1`
  - `fiscal_address_city`
  - `fiscal_address_postal_code`
  - `fiscal_address_country`
  - `email`
  - `land_line`
  - `land_line_country_code`
  - `mobile`
  - `mobile_country_code`
  - `created_at`
  - `created_by`
  - `updated_at`
  - `updated_by`
  - `deleted_at`
  - `deleted_by`

Code/table/column names are defined in English.

## 2) EntityType

- Description: Closed classification for owner legal type.
- Allowed values:
  - `PERSONA_FISICA`
  - `PERSONA_JURIDICA`
  - `ESPJ`
- Validation rules:
  - Any other value is invalid and results in typed validation error.

## Relationships

- This feature defines no inter-entity relationship with properties/contracts yet.
- Future references from `F-0003` and `F-0006` will use `owner_id` as stable foreign reference.

## State model

1. Active:
  - `deleted_at = null`
  - visible in list/detail with default filters

2. Soft deleted:
  - `deleted_at != null`
  - hidden by default in list/detail
  - retrievable only when `include_deleted = true`
  - not editable

## State transitions

1. Create owner:
  - Input validated, `tax_id` normalized.
  - Owner created in active state.

2. Update owner:
  - Allowed only in active state.
  - `owner_id` immutable.
  - `updated_at` and `updated_by` refreshed.

3. Soft delete owner:
  - Allowed only in active state.
  - Set `deleted_at` and `deleted_by`.
  - No hard delete.

4. Read/list with include_deleted:
  - `include_deleted = false` (default): active only.
  - `include_deleted = true`: active + deleted.

## Invariants

- UTC-only timestamps for all audit date-time fields.
- Typed error model and deterministic HTTP mapping.
- Logs contain no owner PII.
- No economic ledger semantics apply in this feature.