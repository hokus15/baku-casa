# Research - F-0002 Propietarios (Sujetos Fiscales)

## 1) tax_id normalization for uniqueness and search

- Decision: Normalize `tax_id` before validation, persistence, uniqueness checks, and exact-tax_id filtering using: trim, uppercase, remove internal spaces, remove hyphens.
- Rationale: Prevent semantic duplicates caused by formatting variants and keep deterministic behavior for create/update/search flows.
- Alternatives considered:
  - Literal comparison without normalization: rejected because it allows duplicates such as `12345678-z` vs `12345678Z`.
  - Partial normalization (trim + uppercase only): rejected because spaces/hyphens still break uniqueness consistency.

## 2) Soft-delete audit fields and actor traceability

- Decision: Require `created_by`, `updated_by`, and `deleted_by` as audit actor fields in addition to UTC timestamps.
- Rationale: Constitution requires auditable mutable entities and explicit soft-delete audit in non-economic data.
- Alternatives considered:
  - Keep only `deleted_at`: rejected due to constitutional non-compliance.
  - Keep actor fields internal-only: rejected due to accepted clarification requiring API exposure for these fields.

## 3) include_deleted contract behavior

- Decision: Support `include_deleted` in both list and detail retrieval endpoints with default `false`.
- Rationale: Removes ambiguity between endpoints and ensures predictable API contract behavior.
- Alternatives considered:
  - Allow only in list: rejected due to inconsistent contract semantics.
  - Separate endpoint for deleted records: rejected as unnecessary contract expansion for MVP1.

## 4) Error model and mapping for owner workflows

- Decision: Reuse typed error model with stable English error codes and Spanish messages; map validation to 400, auth to 401, not found to 404, and conflicts to 409.
- Rationale: Required by Constitution and ADR-0009, keeps error surface predictable and contract-testable.
- Alternatives considered:
  - Generic internal exceptions mapped to 500: rejected due to unstable contract behavior.
  - Spanish error codes: rejected due to required English machine codes.

## 5) Observability without PII

- Decision: Exclude owner PII from logs (`tax_id`, first_name, last_name, legal_name, email, land_line, mobile, stamp_image, fiscal address) and log only technical metadata (`owner_id`, `correlation_id`, error_code, operation, result).
- Rationale: EN-0200 and Constitution require structured logs while preventing PII exposure by default.
- Alternatives considered:
  - Include PII in debug logs: rejected to avoid environment-dependent behavior and leakage risk.
  - Mask only part of PII: rejected because clear no-PII rule is simpler and safer.

## 6) Contract versioning impact

- Decision: Introduce owner API as additive surface within `/api/v1`, no MAJOR version increment.
- Rationale: No existing endpoint is removed or behavior-broken; fully aligned with ADR-0004 and ADR-0006.
- Alternatives considered:
  - New MAJOR for owner endpoints: rejected as unnecessary for additive change.

## 7) Identity/contact model evolution

- Decision: Adopt `entity_type` and expand owner payload with `first_name`, `last_name`, `stamp_image`, `land_line`, `land_line_country_code`, `mobile`, and `mobile_country_code`.
- Rationale: Aligns F-0002 with the updated fiscal-subject data model and keeps field naming coherent with domain semantics.
- Alternatives considered:
  - Keep legacy schema shape: rejected due to drift against current feature specification.
  - Introduce parallel legacy/new fields indefinitely: rejected because it adds ambiguity and maintenance overhead for v1.

## Result

No unresolved clarifications remain for F-0002. All `NEEDS CLARIFICATION` points are resolved.