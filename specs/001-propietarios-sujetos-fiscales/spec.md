# Feature Specification: F-0002 — Propietarios (Sujetos Fiscales)

**Feature Branch**: `001-propietarios-sujetos-fiscales`  
**Created**: 2026-03-07  
**Status**: Draft  
**Roadmap Item**: F-0002  
**Phase**: MVP1

## Context and Scope

F-0002 introduces owners (propietarios) as the first master data entity of the domain. An owner is a fiscal subject — individual or legal entity — that may be associated with properties, contracts, and fiscal reports in future features. This feature establishes the owner record as a stable, referenceable identity within the system.

No financial records are created, modified, or queried in this feature. Owners are pure master data.

---

## Clarifications

### Session 2026-03-07

- Q: Should `deleted_by` be recorded and exposed in API for owner soft delete auditing? → A: Yes, register `deleted_by` and expose it in API when applicable.
- Q: Should `created_by` and `updated_by` also be required and exposed in API? → A: Yes, require and expose both fields.
- Q: How should `tax_id` uniqueness treat formatting differences? → A: Normalize with trim, uppercase, remove spaces, and remove hyphens before validation and persistence.
- Q: Should `include_deleted` be supported in both list and detail retrieval? → A: Yes, support it in both endpoints, defaulting to false.
- Q: Can owner PII be included in logs for observability? → A: No, logs must exclude owner PII and use only technical/audit-safe identifiers.

---

## Baseline Enablers Applied

The following completed Enablers are part of the system baseline and this feature MUST integrate with all of them:

| Enabler | Scope | Impact on this Feature |
|---------|-------|------------------------|
| EN-0100 | Project Bootstrap | Base project structure and tooling |
| F-0001 | Authentication | All endpoints MUST require valid JWT authentication |
| EN-0202 | Configuration System | Centralized configuration, fail-fast on invalid settings |
| EN-0200 | Logging Baseline | Structured logging with `correlation_id`, UTC timestamps |
| EN-0201 | In-Memory DB Testing | Integration tests use in-memory database; no real DB required in test suite |
| EN-0300 | HTTP Composition Root | HTTP bootstrap is modular; new owner controller MUST be wired through the established composition root |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Registrar un propietario (Priority: P1)

An authenticated operator wants to register a new fiscal subject (individual or legal entity) as an owner in the system, so that this owner can later be associated with properties, contracts and fiscal documents.

**Why this priority**: Creating owners is the foundational operation of this feature. Without it, no other owner operation is possible.

**Independent Test**: Can be tested end-to-end by registering a new owner via the API and verifying the owner is returned with a stable, unique `owner_id` and all provided fields are persisted correctly.

**Acceptance Scenarios**:

1. **Given** an authenticated operator and no existing owner with the same tax_id, **when** the operator submits a valid create-owner request with all required fields and `entity_type = PERSONA_FISICA`, **then** the system creates the owner, assigns a stable opaque `owner_id`, records `created_at` and `updated_at` in UTC, and returns the full owner representation.
2. **Given** an authenticated operator and no existing owner with the same tax_id, **when** the operator submits a valid create-owner request with `entity_type = PERSONA_JURIDICA` and omits optional contact fields, **then** the system creates the owner successfully with contact fields absent.
3. **Given** an authenticated operator and an existing active owner with tax_id `B12345678`, **when** the operator attempts to register a new owner with the same tax_id, **then** the system rejects the request with a conflict error (typed `CONFLICT`) and no new owner is created.
4. **Given** an unauthenticated request, **when** the operator attempts to create an owner, **then** the system rejects the request with a 401 response.
5. **Given** an authenticated operator, **when** the operator submits a create-owner request with an unrecognized `entity_type` value, **then** the system rejects the request with a validation error (typed `VALIDATION_ERROR`).
6. **Given** an authenticated operator, **when** the operator submits a create-owner request omitting a required field (e.g., `tax_id`), **then** the system rejects the request with a validation error describing the missing field.

---

### User Story 2 — Consultar el detalle de un propietario (Priority: P2)

An authenticated operator wants to retrieve the full details of a specific owner by their identifier, to review or verify information.

**Why this priority**: Detail retrieval is the primary consumption path for owner data and is a prerequisite for editing and for future associations.

**Independent Test**: Can be tested by registering an owner and then retrieving it by `owner_id`, verifying all fields match.

**Acceptance Scenarios**:

1. **Given** an existing active owner, **when** an authenticated operator requests the owner by `owner_id`, **then** the system returns the full owner representation including all persisted fields and audit metadata.
2. **Given** an `owner_id` that does not exist, **when** an authenticated operator requests that owner, **then** the system returns a `NOT_FOUND` error.
3. **Given** an owner that has been soft-deleted, **when** an authenticated operator requests it by `owner_id` without specifying `include_deleted`, **then** the system returns a `NOT_FOUND` error.
4. **Given** an unauthenticated request, **when** attempting to retrieve an owner, **then** the system returns a 401 response.

---

### User Story 3 — Listar y buscar propietarios (Priority: P3)

An authenticated operator wants to obtain a paginated list of active owners, optionally filtered by tax_id or name fragment, to locate or review registered owners.

**Why this priority**: Listing enables navigation of the owner dataset and will be required by future features (e.g., selecting an owner when registering a property).

**Independent Test**: Can be tested by creating several owners and verifying that the list returns them paginated, that tax_id and name filters narrow the results correctly, and that soft-deleted owners are excluded by default.

**Acceptance Scenarios**:

1. **Given** multiple active owners registered, **when** an authenticated operator requests the owner list without filters, **then** the system returns a paginated response containing all active owners with consistent pagination metadata (total, page, page_size).
2. **Given** multiple owners including some with a specific tax_id fragment, **when** the operator filters by `tax_id`, **then** only owners matching that tax_id are returned.
3. **Given** multiple owners including some with similar names, **when** the operator filters by partial `legal_name`, **then** only owners whose name contains the fragment are returned (case-insensitive).
4. **Given** a mix of active and soft-deleted owners, **when** the operator requests the list without `include_deleted`, **then** only active owners appear.
5. **Given** a mix of active and soft-deleted owners, **when** the operator requests the list with `include_deleted = true`, **then** both active and deleted owners are returned, with their `deleted_at` values visible.
6. **Given** a request with `page_size` exceeding the system maximum, **when** the operator requests the list, **then** the system caps `page_size` to the defined maximum and returns results accordingly.
7. **Given** an unauthenticated request, **when** attempting to list owners, **then** the system returns a 401 response.

---

### User Story 4 — Editar un propietario (Priority: P4)

An authenticated operator wants to update the data of an existing owner to correct or extend the information (e.g., update address, change contact email).

**Why this priority**: Edit is needed to maintain accurate master data but depends on create and read being stable first.

**Independent Test**: Can be tested by creating an owner, updating its address, and verifying the detail endpoint reflects the change with an updated `updated_at` value.

**Acceptance Scenarios**:

1. **Given** an existing active owner, **when** an authenticated operator submits an update with valid new data for editable fields, **then** the system persists the changes, updates `updated_at` in UTC, and returns the updated owner representation.
2. **Given** a request to update `owner_id`, **when** the operator includes `owner_id` as a modified field, **then** the system rejects the request or ignores the field, preserving the original `owner_id` unchanged.
3. **Given** an existing active owner with tax_id `A11111111`, **when** the operator updates the tax_id to a value already used by another active owner, **then** the system rejects the request with a `CONFLICT` error.
4. **Given** an `owner_id` that does not exist, **when** an authenticated operator submits an update, **then** the system returns a `NOT_FOUND` error.
5. **Given** a soft-deleted owner, **when** an authenticated operator submits an update, **then** the system returns a `NOT_FOUND` error (deleted owners are not editable).
6. **Given** an unauthenticated request, **when** attempting to update an owner, **then** the system returns a 401 response.

---

### User Story 5 — Eliminar un propietario (soft delete) (Priority: P5)

An authenticated operator wants to remove an owner from active master data without destroying the historical record, so that the owner identifier remains resolvable in historical reports.

**Why this priority**: Soft delete is a safety requirement for future referential integrity (once properties and contracts are introduced, hard deletes would violate historical traceability).

**Independent Test**: Can be tested by creating an owner, soft-deleting it, and verifying it no longer appears in default list results but is retrievable via `include_deleted`.

**Acceptance Scenarios**:

1. **Given** an existing active owner, **when** an authenticated operator requests soft delete, **then** the system sets `deleted_at` (UTC) on the owner and the owner no longer appears in default list results.
2. **Given** an already soft-deleted owner, **when** an authenticated operator requests soft delete again, **then** the system returns a `NOT_FOUND` error (idempotent behavior via 404).
3. **Given** an `owner_id` that does not exist, **when** an authenticated operator requests soft delete, **then** the system returns a `NOT_FOUND` error.
4. **Given** a soft-deleted owner, **when** an authenticated operator retrieves the owner list with `include_deleted = true`, **then** the deleted owner appears with `deleted_at` set.
5. **Given** an unauthenticated request, **when** attempting to soft-delete an owner, **then** the system returns a 401 response.

---

### Edge Cases

- What happens when creating an owner with a tax_id that was used by a previously soft-deleted owner (including exact matches and formatting variants)? The tax_id uniqueness constraint applies only to active (non-deleted) owners; a tax_id from a soft-deleted owner MUST be re-usable for a new active owner.
- What happens when `page = 0` or a negative page number is requested? The system MUST reject the request with a `VALIDATION_ERROR`.
- What happens when `fiscal_address_country` is omitted? The system MUST default to `ES`.
- What happens when `email`, `land_line`, or `mobile` are provided as empty strings? The system MUST treat them as absent (null/omitted), not as valid contact data.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow an authenticated operator to create a new owner with the required fields: `entity_type`, `first_name`, `last_name`, `legal_name`, `tax_id`, `fiscal_address_line1`, `fiscal_address_city`, `fiscal_address_postal_code`.
- **FR-024**: The system MUST accept optional `stamp_image` on create and update; when omitted or null it MUST be treated as absent.
- **FR-002**: The system MUST apply a default value of `ES` for `fiscal_address_country` when not provided.
- **FR-003**: The system MUST accept optional contact fields `email`, `land_line`, `land_line_country_code`, `mobile`, and `mobile_country_code` on create and update. Empty or absent contact fields MUST be stored as absent.
- **FR-004**: The system MUST assign a stable, opaque, immutable `owner_id` to each owner on creation. This identifier MUST NOT encode any semantic information.
- **FR-005**: The system MUST enforce tax_id uniqueness among all active (non-soft-deleted) owners using a normalized tax_id value. A tax_id MUST be reusable for a new owner if the previous owner holding that tax_id has been soft-deleted.
- **FR-006**: The system MUST validate `entity_type` against the closed set `{PERSONA_FISICA, PERSONA_JURIDICA, ESPJ}` and reject any other value with a `VALIDATION_ERROR`.
- **FR-007**: The system MUST persist audit fields `created_at`, `created_by`, `updated_at`, and `updated_by` for every owner. Timestamps MUST be UTC and `updated_at` plus `updated_by` MUST be refreshed on every update operation.
- **FR-008**: The system MUST allow an authenticated operator to retrieve a single owner by `owner_id`. By default (`include_deleted = false`), soft-deleted owners MUST NOT be returned. When `include_deleted = true`, a soft-deleted owner MAY be returned.
- **FR-009**: The system MUST allow an authenticated operator to retrieve a paginated list of owners. The response MUST include pagination metadata: total count, current page, and page size.
- **FR-010**: The system MUST enforce a maximum allowed `page_size` for list queries. Requests exceeding the maximum MUST be capped silently to the maximum.
- **FR-011**: The system MUST support filtering the owner list by exact `tax_id` match and by partial case-insensitive `legal_name` match. Both filters are independently optional and MAY be combined.
- **FR-012**: The system MUST exclude soft-deleted owners from list and search results by default (`include_deleted = false`). An explicit `include_deleted = true` parameter MAY be used to include them.
- **FR-013**: The system MUST allow an authenticated operator to update editable fields of an existing active owner. `owner_id` MUST be immutable and MUST NOT be modifiable via update.
- **FR-014**: The system MUST perform soft delete on an owner by recording `deleted_at` (UTC) and `deleted_by` (actor identifier). No owner record MUST be permanently destroyed.
- **FR-015**: The system MUST return a `NOT_FOUND` error when an operation targets an `owner_id` that either does not exist or belongs to a soft-deleted owner (unless `include_deleted` is in scope).
- **FR-016**: All owner management endpoints MUST require a valid authenticated token. Unauthenticated requests MUST be rejected with a 401 response. The authentication mechanism is defined by F-0001 and ADR-0005.
- **FR-017**: All error responses MUST include a stable machine-readable error code in English and a descriptive human-readable message in Spanish, conforming to ADR-0009. Error responses MUST include the `correlation_id` of the request.
- **FR-018**: All log entries produced by owner operations MUST include `correlation_id`, conforming to EN-0200.
- **FR-019**: API representations that include soft-deleted owners (detail or list with `include_deleted = true`) MUST expose `deleted_by` together with `deleted_at`.
- **FR-020**: API representations for owner resources MUST expose `created_by` and `updated_by` together with `created_at` and `updated_at`.
- **FR-021**: Before validation and persistence, `tax_id` MUST be normalized by applying: trim, uppercase transformation, removal of internal spaces, and removal of hyphens. Uniqueness checks MUST use the normalized value.
- **FR-022**: The `include_deleted` query parameter MUST be supported by both `GET /api/v1/owners` and `GET /api/v1/owners/{owner_id}`, with default value `false`.
- **FR-023**: Logs generated by owner operations MUST NOT include owner PII fields (`tax_id`, `first_name`, `last_name`, `legal_name`, `email`, `land_line`, `mobile`, `stamp_image`, fiscal address fields). Logs MUST use `owner_id`, `correlation_id`, error codes, and technical metadata only.

---

### Constitution Alignment *(mandatory)*

- **CA-001**: This feature introduces a new domain entity (Owner / Propietario) spanning all four architectural layers as mandated by ADR-0002:
  - **Domain**: Owner entity, EntityType enumeration, business invariants (tax_id uniqueness rule, immutability of `owner_id`, soft-delete policy). No framework dependencies.
  - **Application**: Owner use cases (create, read, list, update, soft-delete). Repository port defined as interface. No framework-specific code.
  - **Interfaces (Adapters)**: HTTP controller under `/api/v1/owners`, request/response DTOs. No business logic.
  - **Infrastructure**: ORM model for `owners` table, SQLAlchemy repository implementation, schema migration.

- **CA-002**: Contract surface is **changed** (additive). New HTTP resource `/api/v1/owners` is introduced within the existing `v1` major version. All changes are additive; no existing endpoints are modified. No major-version increment required. Future breaking changes to this resource would require incrementing to `v2`.

- **CA-003**: The following contract tests MUST be defined:
  - `POST /api/v1/owners`: happy path (PERSONA_FISICA, PERSONA_JURIDICA, ESPJ), duplicate tax_id rejection, invalid `entity_type`, missing required fields, unauthenticated.
  - `GET /api/v1/owners/{owner_id}`: found, not found, soft-deleted without `include_deleted`, unauthenticated.
  - `GET /api/v1/owners`: paginated list, tax_id filter, name filter, `include_deleted` flag, page_size cap, unauthenticated.
  - `PATCH /api/v1/owners/{owner_id}`: valid update, tax_id conflict, not found, soft-deleted owner, `owner_id` immutability, unauthenticated.
  - `DELETE /api/v1/owners/{owner_id}`: soft delete, repeat soft-delete (404), not found, unauthenticated.

- **CA-004**: This feature involves no monetary values and no percentage types. Audit timestamps (`created_at`, `updated_at`, `deleted_at`) MUST be stored in UTC and serialized as ISO 8601 strings in the API, per ADR-0012 and the Constitution. Audit actor fields (`created_by`, `updated_by`, `deleted_by`) are mandatory for their respective operations.

- **CA-005**: Documentation update required:
  - `backend/README.md` MUST document the new owner endpoints.
  - `docs/spec/roadmap.md` and `docs/spec/dependency-graph.yaml` MUST be updated to reflect status transition (`planned → in_progress → done`).

- **CA-006**: All functional changes MUST follow TDD: tests MUST be written before implementation (red → green → refactor). Required test tiers: domain unit tests, application use case tests, integration tests (in-memory SQLite per EN-0201), HTTP contract tests.

- **CA-007**: No new constitutional rule gaps are introduced by this feature. The existing global constitution ADR gap for explicit TDD governance remains tracked outside F-0002 scope; all applicable architectural/runtime rules for this feature are covered by existing ADRs (ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0009, ADR-0012).

---

### Key Entities

- **Owner (Propietario)**: The central entity of this feature. Represents a fiscal subject (individual or legal entity) that the operator manages. Key attributes:
  - `owner_id` — stable, opaque, immutable identifier assigned on creation
  - `entity_type` — closed enumeration: `PERSONA_FISICA`, `PERSONA_JURIDICA`, `ESPJ`
  - `first_name` — owner first name (for natural persons)
  - `last_name` — owner last name (for natural persons)
  - `legal_name` — full name or registered company name
  - `tax_id` — fiscal identifier; unique among active owners
  - `stamp_image` — optional/base64 image payload used as owner stamp/signature representation
  - `fiscal_address_line1`, `fiscal_address_city`, `fiscal_address_postal_code`, `fiscal_address_country` — fiscal address
  - `email`, `land_line`, `land_line_country_code`, `mobile`, `mobile_country_code` — optional contact information; informational only, not part of identity
  - `created_at`, `updated_at` — UTC audit timestamps, mandatory
  - `created_by`, `updated_by` — actor identifiers for create and update operations, mandatory
  - `deleted_at` — UTC soft-delete timestamp; absent for active owners
  - `deleted_by` — actor identifier of the delete operation; absent for active owners

- **EntityType**: Closed enumeration with exactly three values: `PERSONA_FISICA`, `PERSONA_JURIDICA`, and `ESPJ`. No other value is valid.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator can register a new owner via the API and receive a confirmation with a stable `owner_id` and all submitted fields correctly reflected in the response.
- **SC-002**: Attempting to register two owners with the same tax_id results in a clear rejection for the second request, with no duplicate owner persisted.
- **SC-003**: An operator can retrieve the paginated list of active owners; the response faithfully reflects only non-deleted owners, with correct pagination metadata (total, page, page_size).
- **SC-004**: An operator can find an owner by exact tax_id or partial name match; unrelated owners are excluded from results.
- **SC-005**: After a soft delete, the owner no longer appears in default list results and returns `NOT_FOUND` on direct retrieval, but is visible when `include_deleted = true` is used with both `deleted_at` and `deleted_by`.
- **SC-006**: All owner operations correctly enforce authentication; unauthenticated requests receive a 401 response on every endpoint.
- **SC-007**: All error responses include a `correlation_id` linking the response to the originating request log entry.
- **SC-008**: The `owner_id` of any owner never changes across its lifetime, including after successive updates.
- **SC-009**: Owner API representations include `created_by` and `updated_by` consistently, and include `deleted_by` when and only when the owner is soft-deleted.
- **SC-010**: Requests using equivalent `tax_id` variants (for example `12345678-z`, `12345678 Z`, and `12345678z`) are treated as the same identifier for uniqueness and search.
- **SC-011**: With `include_deleted` omitted (or false), deleted owners are not returned in either list or detail endpoints; with `include_deleted = true`, deleted owners can be returned in both endpoints.
- **SC-012**: Operational logs for owner workflows contain no owner PII and still allow traceability through `owner_id` and `correlation_id`.

---

## Dependency Graph Impact

- **Declared dependencies satisfied**: F-0002 explicitly depends on F-0001 (done). All applicable MVP0 Enablers (EN-0100, EN-0202, EN-0200, EN-0201, EN-0300) are done.
- **No forward dependencies**: F-0002 does NOT depend on any features or enablers that are `planned` or not yet started. No implicit dependencies introduced.
- **Downstream features**: F-0003, F-0006 directly depend on F-0002. This feature's `owner_id` will serve as a foreign reference in those features. This feature MUST ensure `owner_id` is stable and immutable.
- **Status update required**: `docs/spec/dependency-graph.yaml` and `docs/spec/roadmap.md` MUST be updated to reflect the status transition of F-0002 from `planned` to `in_progress` when development begins, and to `done` on completion.

---

## ADR Gap

No ADR gaps identified. All design decisions in this feature are governed by existing ADRs:

| ADR | Material Impact |
|-----|----------------|
| ADR-0002 | Hexagonal architecture applied: new Owner entity across all four layers |
| ADR-0003 | New `owners` ORM model and schema migration required |
| ADR-0004 | New resource `/api/v1/owners` introduced; pagination and versioning rules apply |
| ADR-0005 | All owner endpoints require JWT authentication established by F-0001 |
| ADR-0006 | New HTTP contract added to v1; additive change, no breaking modifications |
| ADR-0009 | Typed error model applied: VALIDATION_ERROR, NOT_FOUND, CONFLICT |
| ADR-0012 | UTC timestamps required for `created_at`, `updated_at`, `deleted_at` |

---

## Architectural Impact

| Concern | Impact |
|---------|--------|
| HTTP Contracts | New resource `/api/v1/owners` (POST, GET collection, GET by id, PATCH, DELETE). Additive to v1. |
| Persistence | New `owners` table. Schema introduced via versioned migration. |
| Domain Events | None. No events are published in this feature. |
| Configuration | None. No new configuration keys required. |
| Error Model | No new error categories. Existing typed error codes (VALIDATION_ERROR, NOT_FOUND, CONFLICT, UNAUTHORIZED) applied. |
| Versioning Impact | Additive to `/api/v1`. No breaking changes. No major version increment needed. |

---

## Out of Scope

- Owner ↔ Property relationship (introduced in F-0003).
- Advanced tax_id/VAT format validation by country.
- Multi-user access or per-owner permissions.
- Tax calculations or regulatory reporting.
- Integration with external systems or messaging channels referencing `owner_id` (addressed in dedicated features/modules).

---

## Assumptions

- Default country for fiscal address is `ES` (Spain) when not specified by the operator, consistent with the system's geographic scope (context.md §2).
- tax_id checksum or country-specific fiscal validity is out of scope; however, the tax_id string is normalized (trim, uppercase, no spaces, no hyphens) before validation, storage, and uniqueness checks.
- Pagination defaults (default page size, maximum page size) are to be defined at implementation time; the spec requires consistent enforcement of a bounded maximum.
- Audit actor fields (`created_by`, `updated_by`, `deleted_by`) are captured from the authenticated actor identity defined by F-0001.

---

## Documentation Updates Required

| Document | Required Change |
|----------|----------------|
| `backend/README.md` | Document new owner endpoints |
| `docs/spec/roadmap.md` | Update F-0002 status from `planned` to `in_progress` / `done` |
| `docs/spec/dependency-graph.yaml` | Update F-0002 status accordingly |
