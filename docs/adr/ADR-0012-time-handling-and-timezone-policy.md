# ADR-0012: Time Handling and Timezone Policy

## Status
Accepted

## Context

The system handles:

- Contract start/end dates
- Accrual periods
- Payment timestamps
- Audit fields
- Event timestamps
- Token expiration

Time inconsistencies can cause:

- Financial errors
- Invariant violations
- Hard-to-debug bugs

A strict and consistent time policy is required.

---

## Decision

### Internal Representation

All timestamps SHALL:

- Be stored in UTC.
- Be timezone-aware.
- Use ISO 8601 format when serialized.

Naive datetime objects are forbidden.

---

### Domain Rules

- Domain logic MUST operate in UTC.
- No implicit timezone conversions inside domain layer.
- Date-only concepts (e.g., billing month) MUST be explicitly modeled as date types, not datetime.

---

### Persistence

- Database MUST store timestamps in UTC.
- Audit fields:
  - created_at
  - updated_at
  - deleted_at
  MUST be UTC.

---

### API Layer

- API responses MUST use ISO 8601 UTC timestamps.
- Client-side timezone presentation is out of scope.
- Timezone conversion MUST NOT occur inside the backend.

---

### Event Layer (CloudEvents)

- CloudEvents `time` attribute MUST be RFC3339 UTC.
- Correlation timestamps MUST be UTC.

---

### JWT

- `iat` and `exp` MUST use UTC.
- Clock skew tolerance MUST be bounded and explicit.

---

## Alternatives Considered

### 1. Store Local Time

Rejected because:
- Ambiguous DST handling.
- Region-dependent behavior.

### 2. Mixed Timezones

Rejected because:
- Inconsistent domain logic.
- Difficult debugging.

---

## Consequences

### Positive

- Deterministic time handling.
- No DST ambiguity.
- Cross-system consistency.

### Negative / Trade-offs

- Requires strict discipline.
- Explicit timezone handling required at boundaries.

---

## Verification

- Tests must validate timezone-aware datetimes.
- No naive datetime allowed.
- Serialization must produce ISO 8601 UTC.

---

## Plan Enforcement

Any feature introducing date/time logic MUST:

- Explicitly define timezone behavior.
- Use UTC internally.
- Ensure ISO 8601 compliance in API and events.

If naive datetime is introduced, the plan is invalid.
If naive datetime is introduced, the plan is invalid.