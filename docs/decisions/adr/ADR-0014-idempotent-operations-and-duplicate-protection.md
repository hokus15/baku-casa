# ADR-0014: Idempotent Operations and Duplicate Protection

## Status
Accepted

## Context

The system manages economic operations including:

- accrual generation
- payments
- invoices
- ledger entries

These operations create persistent financial effects and MUST remain consistent even in the presence of retries, network failures or operator mistakes.

Without protection against duplicate operations the system could produce:

- duplicated ledger entries
- duplicated payments
- incorrect balances

A clear strategy is required to guarantee safe retries.

## Decision

Operations that generate economic effects MUST be safe against retries.

The system SHALL implement mechanisms to prevent duplicate execution of critical operations.

These mechanisms MAY include:

- idempotency keys
- uniqueness constraints
- application-level duplicate detection

The system MUST ensure that repeated execution of the same logical operation does not create duplicated economic effects.

The canonical business scope of this ADR includes at least:

- accrual creation
- payment registration
- payment application
- invoice creation when it creates persistent financial state

Each protected flow MUST define what constitutes the same logical operation before implementation begins.

## Operational Interpretation (Binding)

### Logical Operation Identity

A protected flow MUST define a stable identity for the operation being retried.

That identity MAY be expressed through:

- an explicit idempotency key
- a deterministic uniqueness constraint
- a canonical application-level fingerprint

The chosen mechanism MUST distinguish between:

- a true retry of the same operation
- a new legitimate operation with similar business data

### Expected Behavior on Retry

When the system receives the same logical operation again, it MUST do exactly one of the following:

- return the already-created result
- reject the operation deterministically as a duplicate

It MUST NOT create additional persistent financial effects.

If the same idempotency identity is reused with materially different parameters, the operation MUST be rejected as invalid rather than treated as a successful retry.

### Layering Discipline

Duplicate-protection rules MAY be enforced in application services, persistence constraints, or both.

The Domain layer MAY declare invariants that require uniqueness of business effects, but it MUST NOT depend on infrastructure-specific retry mechanisms or transport-specific idempotency adapters.

### Observability

Protected flows MUST emit enough operational information to diagnose:

- duplicate detection
- retry reuse of prior results
- rejection due to conflicting parameters

Observability of these outcomes MUST follow ADR-0009 and reuse correlation identifiers consistently across the protected flow.

## Consequences

### Positive

- Safe retries in APIs and automation.
- Protection of ledger integrity.
- Reduced operational risk.

### Negative

- Additional complexity in application services.
- Need to define which operations require idempotency.

## Verification

Compliance is validated by:

- tests that retry the same protected operation and prove that no duplicate economic effect is created
- tests that reuse the same identity with incompatible parameters and verify deterministic rejection
- tests that confirm duplicate or retry outcomes remain observable in logs or equivalent operational traces

## Rules (Binding)

- Operations that create economic events MUST protect against duplication.
- Idempotency MUST be implemented at the application layer or persistence layer where appropriate.
- The Domain layer MUST remain free of infrastructure-specific idempotency mechanisms.
- Every protected flow MUST define the identity of a repeated logical operation explicitly in its spec or implementation plan.
- A repeated logical operation MUST never create a second economic effect.
