# ADR-0006: Contract Versioning and Cross-Root Integration Discipline

## Status
Accepted

## Context

The system follows a monorepo multi-root architecture (see ADR-0001) where:

- Runtime shared code between roots is forbidden.
- Direct imports across roots are not allowed.
- Integration must occur exclusively via explicit contracts.

The system exposes an HTTP API (see ADR-0004) and may emit domain events to external consumers (e.g., bot or future components).

To preserve architectural boundaries and long-term maintainability, all integration mechanisms must be:

- Explicit
- Versioned
- Testable
- Backward-compatible within a major version

A formal contract discipline is required for both synchronous (HTTP) and asynchronous (event-driven) integration.


## Decision

Integration between roots and external components SHALL occur exclusively through **explicit, versioned contracts**.

Contracts may be:

- HTTP APIs (OpenAPI specification)
- Event contracts (Webhooks or MQTT messages using CloudEvents format)

No other integration mechanism is permitted.

---

## Contract Definition

A contract MUST:

- Be explicitly documented.
- Be versioned using semantic versioning principles.
- Define a stable schema.
- Be independent from internal implementation details.

Breaking changes REQUIRE a MAJOR version increment.

Breaking changes include:

- Removing fields
- Renaming fields
- Changing semantics
- Changing required/optional status incompatibly
- Modifying event payload structure incompatibly

---

## HTTP Contracts (Synchronous)

- The OpenAPI specification is the authoritative contract.
- Consumers MUST rely on the published contract, not internal implementation details.
- The MAJOR version MUST appear in the URL path (`/api/v{major}`).
- Contract tests MUST validate compatibility.
- Backward compatibility MUST be preserved within the same MAJOR version.

---

## Event Contracts (Asynchronous)

The backend MAY publish domain events via:

- Webhooks (HTTP POST)
- MQTT (publish/subscribe)

Both transports are officially supported.

Transport choice MUST NOT alter:

- CloudEvents compliance
- Versioning rules
- Delivery semantics
- Idempotency guarantees

The transport layer is considered infrastructure and MUST remain decoupled from domain logic.

---

### Event Envelope (Binding – CloudEvents)

All events MUST conform to the CloudEvents specification.

Events MUST include at minimum the following CloudEvents attributes:

- `id` (unique event identifier, UUID)
- `source` (origin of the event, e.g., backend service URI)
- `type` (stable, versioned event type identifier)
- `specversion` (CloudEvents specification version)
- `time` (RFC3339 UTC timestamp)

The event payload MUST be carried in the `data` field.

---

### Domain-Specific Event Rules

- The `type` attribute MUST be stable and versioned (e.g., `contract.created.v1`).
- Breaking changes to the event schema REQUIRE a MAJOR version increment in the event type.
- The `data` field MUST contain a versioned schema definition.
- Consumers MUST rely only on the contractually defined CloudEvents structure.
- Event schemas MUST NOT reuse internal domain objects directly.

---

### Delivery Semantics

- Delivery MUST be **at-least-once**.
- Consumers MUST implement idempotency using the CloudEvents `id`.
- Event publication MUST be durable (no event loss on crash).

If durability is required, an outbox pattern MUST be used with persistent storage.

---

### MQTT Requirements (If Used)

If MQTT is used:

- A broker MUST be defined as an OPTIONAL component in Docker Compose using a dedicated profile (e.g., `events`).
- When the MQTT profile is disabled, the system MUST remain fully functional.
- No feature may REQUIRE MQTT unless it explicitly declares it in its implementation plan and references this ADR.
- Topic naming MUST be stable and version-aware (e.g., `baku/contracts/v1/created`).
- Messages MUST carry CloudEvents-compliant payloads.
- QoS level MUST be explicitly defined (at least QoS 1 for at-least-once delivery).
- Consumers MUST implement idempotency based on CloudEvents `id`.
- The system MUST NOT depend on external managed MQTT services unless explicitly allowed by a future ADR.

---

## Cross-Root Isolation

- No root may import Python modules from another root.
- No shared internal package is allowed.
- DTO or schema duplication across roots is acceptable if required to preserve isolation.

---

## Contract Tests (Mandatory)

Contract tests MUST validate compatibility between:

- Consumer root
- Provider root

For HTTP:
- Schema validation against OpenAPI
- Backward compatibility checks

For Events:
- Schema validation against CloudEvents structure
- Validation of required envelope fields
- Sample payload verification

Contract tests MUST run in CI.

A change that breaks a consumer MUST fail CI.

---

## Alternatives Considered

### 1. Shared Internal Library for DTOs or Events

Rejected because:
- Violates root isolation.
- Encourages tight coupling.
- Undermines architectural boundaries.

### 2. Informal Integration (Manual Testing Only)

Rejected because:
- Breakages may go unnoticed.
- Violates reproducibility goals.
- Undermines CI governance.

### 3. No Versioning (Single Evolving Contract)

Rejected because:
- Breaking changes become uncontrolled.
- Consumers become fragile.
- Violates contract stability guarantees.

---

## Consequences

### Positive

- Strong integration discipline.
- Safe evolution of API and event contracts.
- CI-enforced compatibility.
- Clear boundary enforcement aligned with ADR-0001.
- Standardized CloudEvents envelope.
- Optional MQTT without architectural coupling.

### Negative / Trade-offs

- Additional maintenance effort for contract tests.
- DTO/event schema duplication across roots.
- Version management overhead.
- Event durability requires additional persistence logic.
- MQTT introduces optional operational complexity.

### Operational Impact

- CI must execute contract tests across roots.
- Breaking changes require coordinated major version increments.
- OpenAPI and event schemas must be versioned and stored.
- Docker Compose MUST support enabling/disabling MQTT via profiles without changing application binaries.
- If MQTT profile is enabled, broker lifecycle management becomes part of operational responsibility.

---

## Verification

Compliance is validated by:

- Static checks preventing cross-root imports.
- Contract tests executed in CI.
- OpenAPI schema validation.
- CloudEvents schema validation.
- Code review ensuring semantic versioning discipline.
- Tests verifying idempotent event handling.
- Integration tests verifying durability if outbox is implemented.

---

## Plan Enforcement

Any feature implementation plan MUST:

- Explicitly reference this ADR when modifying:
  - HTTP endpoints
  - Event publication
  - Integration surfaces
- Declare whether the change is breaking or non-breaking.
- Update contract versioning accordingly.
- Add or update contract tests proving compatibility.
- If events are introduced, define:
  - CloudEvents structure
  - Delivery semantics
  - Durability strategy
  - Transport selection (Webhook or MQTT)

If a plan violates these rules, it is invalid.