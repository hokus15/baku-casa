# ADR-0010: Event Publication and Delivery Mechanism

## Status
Accepted

## Context

The system may publish domain events (see ADR-0006) using CloudEvents format via:

- Webhooks (HTTP)
- MQTT (optional, via Docker Compose profile `events`)

Constraints:

- Self-hosted deployment.
- SQLite as primary storage (ADR-0003).
- No external managed infrastructure.
- Delivery must be reliable.
- No event loss on crash.
- At-least-once semantics required.
- Consumers must be idempotent.

A deterministic and durable event publication mechanism is required.


## Decision

The system SHALL implement an **Outbox Pattern** backed by SQLite to guarantee durable event publication.

Event delivery semantics SHALL be **at-least-once**.

Event publication is an infrastructure concern and MUST remain decoupled from domain logic.

---

## Outbox Pattern (Binding)

### Persistence

- Events MUST be stored in a persistent `outbox` table within the same transaction as the business state change.
- The outbox insert MUST occur atomically with the domain transaction.
- Publisher transactions MUST be short-lived to avoid SQLite write contention.
- No event may be published without being persisted first.

### Outbox Table Requirements

The outbox table MUST include at minimum:

- `id` (UUID, CloudEvents id)
- `event_type`
- `event_version`
- `payload` (CloudEvents data)
- `created_at` (UTC)
- `published_at` (nullable)
- `retry_count`
- `last_error` (nullable)

Indexes MUST support efficient retrieval of unpublished events.

---

## Publisher Worker

A dedicated publisher mechanism MUST:

- Poll or subscribe to outbox entries.
- Attempt delivery.
- Mark events as published upon success.
- Increment `retry_count` upon failure.
- Record failure reason in `last_error`.

Publisher logic MUST NOT block domain transactions.

---

## Delivery Semantics

- Delivery is **at-least-once**.
- Consumers MUST implement idempotency using CloudEvents `id`.
- No exactly-once guarantee is provided.
- Ordering is NOT guaranteed across aggregates.
- Ordering SHOULD be preserved per aggregate if feasible.

---

## Retry Policy

- Retries MUST use bounded exponential backoff.
- Maximum retry attempts MUST be configurable.
- After exceeding retry limit, events MAY:
  - Remain in failed state
  - Be flagged for manual inspection
- Silent infinite retry loops are forbidden.

---

## Transport-Specific Rules

### Webhooks

If Webhooks are used:

- Delivery MUST use HTTP POST.
- Timeout MUST be bounded.
- Non-2xx responses MUST be treated as failures.
- Optional request signing MAY be implemented.
- Correlation ID MUST be propagated.

### MQTT (Optional Profile)

If MQTT is enabled:

- Broker MUST run inside Docker Compose `events` profile (ADR-0007).
- QoS MUST be at least 1.
- Topic naming MUST be stable and version-aware.
- Reconnection logic MUST be implemented.
- Publication failure MUST trigger retry logic via outbox.

---

## Crash Safety

- If the system crashes after committing business state but before publishing, the event MUST still be delivered upon restart.
- Publisher startup MUST scan and resume pending outbox entries.

---

## Alternatives Considered

### 1. Direct Publish Without Outbox

Rejected because:
- Risk of event loss on crash.
- Violates durability requirement.
- Breaks consistency between state and events.

### 2. In-Memory Queue

Rejected because:
- Not durable.
- Unsafe under restart.
- Violates reproducibility goals.

### 3. Exactly-Once Delivery

Rejected because:
- Operationally complex.
- Requires distributed coordination.
- Overkill for current system scope.

---

## Consequences

### Positive

- Strong durability guarantees.
- Deterministic event behavior.
- Crash-safe publication.
- Clean separation between domain and infrastructure.
- Compatible with SQLite constraint.

### Negative / Trade-offs

- Additional table and background worker complexity.
- Slight increase in write transaction overhead.
- Operational monitoring required for failed events.

---

## Operational Impact

- Database schema includes outbox table.
- Publisher process must run as part of backend service.
- Failed events require observability and monitoring (ADR-0009).
- Backup strategy must include outbox table.

---

## Verification

Compliance is validated by:

- Tests ensuring outbox insert occurs within domain transaction.
- Crash simulation tests verifying event delivery after restart.
- Tests verifying retry behavior.
- Integration tests for MQTT and Webhook delivery.
- CI validation of outbox schema migrations.

---

## Plan Enforcement

Any feature that introduces event publication MUST:

- Reference this ADR.
- Define event type and version.
- Include outbox persistence logic.
- Define retry behavior.
- Include idempotency documentation for consumers.

If a plan publishes events without outbox durability, it is invalid.