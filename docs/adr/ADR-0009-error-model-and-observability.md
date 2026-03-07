# ADR-0009: Error Model and Observability

## Status
Accepted

## Context

The system enforces strict architectural and contract discipline (ADR-0001 to ADR-0008).

Given that:

- The system is self-hosted.
- It runs on constrained hardware.
- It exposes HTTP APIs and may emit events.
- It enforces financial invariants.

Operational visibility and consistent error handling are critical for:

- Debuggability
- Contract stability
- Supportability
- Safe evolution

A unified error and observability model is required.


## Decision

The system SHALL implement a **typed error model** and **structured observability strategy** across all components.

---

## Error Model (Binding)

### Typed Errors

All business and application errors MUST:

- Be explicitly typed (no generic exceptions leaking to API layer).
- Contain a stable machine-readable error code (English).
- Be mapped deterministically to HTTP status codes (see ADR-0004).

Example categories:

- VALIDATION_ERROR
- NOT_FOUND
- CONFLICT
- UNAUTHORIZED
- FORBIDDEN
- INVARIANT_VIOLATION
- INTERNAL_ERROR

Error codes MUST be stable across versions within the same MAJOR API version.

---

### Error Response Format (HTTP)

HTTP error responses MUST include:

- `error_code` (stable machine-readable code)
- `message` (human-readable, Spanish)
- `correlation_id` (trace identifier)

Internal exception details MUST NOT be exposed.

---

### Domain Layer Rules

- Domain errors MUST be defined in the Domain layer.
- Infrastructure exceptions MUST be translated at the Application boundary.
- Controllers MUST NOT construct business errors directly.

---

## Logging Strategy

### Structured Logging

All services MUST use structured logs (JSON or equivalent structured format).

For the Python application components, including `backend` and `bot`, all logging MUST
use the Python standard library `logging` module as the canonical logging framework.

Features and enablers MUST NOT introduce alternative logging libraries as primary logging
mechanisms.

Structured JSON output, human-friendly output, correlation, rotation, retention, and any
logging-specific extensions MUST be implemented on top of the Python `logging` module
using handlers, formatters, filters, adapters, or equivalent integration points.

Wrapper utilities are allowed only if they delegate to the Python `logging` module and
preserve the common logging contract defined by this ADR.

Logs MUST include at minimum:

- timestamp (UTC)
- level
- service name
- correlation_id
- message
- optional contextual fields

---

### Log Storage and Rotation

Services MUST persist logs to file in self-hosted deployments.

Log files MUST rotate daily at **00:00 (Europe/Madrid)**.

Retention MUST be enforced automatically (time-based or file-count based) and MUST be configurable per environment.

Rotation policy MUST NOT affect the log event timestamp policy (timestamps remain UTC).

---

### Log Language

- Log messages MUST be in English.
- Error codes MUST be in English.
- User-facing messages MAY be in Spanish.

---

### Domain Event Logging

Relevant domain events MAY be recorded in the structured logging system to improve functional traceability.

Domain event logs:

- MUST include `correlation_id`
- SHOULD include identifiers of affected domain entities
- MUST NOT replace technical error logs
- MUST NOT implement event sourcing or message publishing

Their purpose is operational observability of business processes.

---

## Correlation and Traceability

- Every incoming HTTP request MUST generate or propagate a `correlation_id`.
- The correlation ID MUST be:
  - Included in logs.
  - Included in error responses.
  - Propagated to outbound HTTP calls and event publications.

For events (CloudEvents):

- The `id` attribute MUST be logged.
- Correlation ID SHOULD be included as an extension attribute if applicable.

---

## Audit Fields

For mutable entities:

- `created_at`
- `updated_at`
- `deleted_at` (if soft-delete is allowed)

Audit fields MUST:

- Be stored in UTC.
- Be managed automatically (not manually by controllers).

Soft delete is allowed only when consistent with domain rules.

---

## Observability Scope

The system MUST support:

- Error rate inspection via logs.
- Event publication traceability.
- Database migration traceability.
- Authentication failure tracking.

External observability platforms are optional and out of scope.

---

## Alternatives Considered

### 1. Ad-hoc Exception Handling

Rejected because:
- Leads to inconsistent error responses.
- Breaks API contract discipline.
- Reduces diagnosability.

### 2. Plain Text Logging

Rejected because:
- Hard to parse programmatically.
- Not scalable for automated analysis.

### 3. Multiple Logging Frameworks in the Same Application

Rejected because:
- Breaks operational consistency across features and enablers.
- Increases maintenance and integration cost.
- Makes shared policies such as correlation, formatting, rotation, and retention harder to enforce.

### 4. Exposing Internal Stack Traces

Rejected because:
- Security risk.
- Breaks contract stability.
- Leaks implementation details.

---

## Consequences

### Positive

- Deterministic error behavior.
- Stable API error contracts.
- Improved debugging.
- Safer evolution of business logic.
- Cross-component traceability.

### Negative / Trade-offs

- Requires explicit error class definitions.
- Slightly more boilerplate in mapping layers.
- Structured logging configuration effort.
- Logging extensions must integrate through Python `logging` instead of choosing independent frameworks.

---

## Operational Impact

- Logs must be persisted or accessible.
- Correlation ID propagation must be implemented consistently.
- Error codes must be version-stable.
- Logging implementation must remain homogeneous across the Python application
  components, including `backend` and `bot`, via the standard `logging` module.

---

## Verification

Compliance is validated by:

- Tests verifying error mapping to HTTP codes.
- Tests ensuring correlation ID presence.
- Static checks preventing generic exception leaks.
- Log format validation in CI.
- Contract tests validating error schema stability.

---

## Plan Enforcement

Any feature implementation plan MUST:

- Define new error types if new failure modes are introduced.
- Define HTTP status mapping for new endpoints.
- Ensure correlation ID propagation.
- Update contract tests if error schemas change.

If a plan violates these rules, it is invalid.
