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

## Consequences

### Positive

- Safe retries in APIs and automation.
- Protection of ledger integrity.
- Reduced operational risk.

### Negative

- Additional complexity in application services.
- Need to define which operations require idempotency.

## Rules (Binding)

- Operations that create economic events MUST protect against duplication.
- Idempotency MUST be implemented at the application layer or persistence layer where appropriate.
- The Domain layer MUST remain free of infrastructure-specific idempotency mechanisms.