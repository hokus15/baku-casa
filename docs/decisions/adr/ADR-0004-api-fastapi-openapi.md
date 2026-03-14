# ADR-0004: HTTP API Architecture (FastAPI + OpenAPI + Versioning)

## Status
Accepted

## Context

The system exposes its functionality through an HTTP API starting from Feature 1.

Key drivers:

- Early access via Postman or equivalent tools.
- Clear, stable, versioned external contracts.
- Strong separation between Domain and transport concerns (see ADR-0002).
- Contract-based integration between roots (see ADR-0001).
- Typed error model and reproducible behavior across implementations.

The API must be explicit, versioned, and self-documented.


## Decision

The system SHALL use:

- **FastAPI** as the HTTP adapter framework.
- **OpenAPI** as the authoritative API contract.
- Explicit URI-based versioning using `/api/v{major}`.

Example:
`/api/v1/contracts`
`/api/v1/payments`

### Versioning Rules (Binding)

- The MAJOR version MUST be expressed in the URL path.
- Breaking changes REQUIRE a MAJOR version increment.
- Within the same MAJOR version:
  - Fields MAY be added (optional only).
  - Fields MUST NOT be removed or renamed.
  - Semantics MUST NOT change.

### OpenAPI as Source of Truth

- The generated OpenAPI specification MUST reflect the real contract.
- The OpenAPI schema MUST be published and versioned.
- Contract tests MUST validate compatibility between versions.

### REST Discipline

- Endpoints MUST be resource-oriented.
- HTTP verbs MUST follow semantic meaning:
  - GET → read
  - POST → create
  - PUT/PATCH → update
  - DELETE → delete (logical when required by domain rules)
- List endpoints MUST support pagination.

### Pagination Rules

- Pagination is mandatory for collection endpoints.
- The API MUST expose:
  - page (or cursor)
  - page_size (bounded by a maximum limit)
- Default and maximum page sizes MUST be defined.

### DTO Separation

- API DTOs MUST be distinct from:
  - Domain models
  - ORM models
- Mapping between DTO ↔ Application ↔ Domain MUST be explicit.
- Business logic MUST NOT exist in controllers.

### Error Mapping

- Typed domain/application errors MUST map to appropriate HTTP status codes:
  - 400 → validation errors
  - 401 → unauthenticated
  - 403 → unauthorized
  - 404 → not found
  - 409 → conflict (e.g., concurrency or invariant violation)
  - 500 → unexpected system error

- Error responses MUST include:
  - Stable machine-readable error code (English)
  - Human-readable message (Spanish)
  - Correlation identifier


This decision is normative and binding.


## Alternatives Considered

### 1. Flask Instead of FastAPI

Rejected because:
- Weaker native OpenAPI integration.
- More manual schema management.
- Less strict typing support.

### 2. Header-Based Versioning

Rejected because:
- Less explicit in URL.
- Harder to test manually with tools like Postman.
- Less transparent for contract review.

### 3. GraphQL Instead of REST

Rejected because:
- Adds complexity.
- Overkill for current domain scope.
- Harder to enforce strict contract versioning rules.


## Consequences

### Positive

- Explicit, stable API contracts.
- Strong typing and validation.
- Automatic OpenAPI documentation.
- Clean separation between transport and business logic.
- Early manual testing capability from Feature 1.

### Negative / Trade-offs

- Versioning requires discipline and governance.
- DTO duplication increases mapping code.
- OpenAPI changes must be carefully reviewed.

### Operational Impact

- API documentation must be versioned and published.
- CI must validate OpenAPI schema integrity.
- Breaking changes require coordinated version increments.

### Verification

Compliance is validated by:

- Automated OpenAPI schema validation in CI.
- Contract tests across versions.
- Code review ensuring no business logic in controllers.
- Static checks preventing Domain imports in API adapters.


## Plan Enforcement

Any feature implementation plan MUST:

- Place all HTTP concerns in an adapter layer.
- Respect URI-based versioning.
- Define pagination when exposing collections.
- Explicitly define error mapping for each new endpoint.
- Update and validate the OpenAPI contract.

If a plan violates these rules, it is invalid.