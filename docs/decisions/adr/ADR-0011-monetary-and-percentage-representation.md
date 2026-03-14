# ADR-0011: Monetary and Percentage Representation

## Status
Accepted

## Context

The system manages financial data including:

- Rents
- Accruals
- Payments
- Ledger balances
- Taxes
- Percentage-based calculations

Financial correctness and determinism are critical.

Floating point arithmetic is unsafe for monetary values and percentages.

The Constitution mandates:

- Percentages MUST be represented in the range 0–100 across all layers.
- Fractional representation (0–1) is forbidden as a domain or persistent model.

A consistent numeric representation strategy is required across:

- Domain
- Persistence
- API
- Events


## Decision

### Monetary Values

All monetary amounts SHALL:

- Be represented using `Decimal` in the Domain layer.
- Never use `float`.
- Define explicit precision and scale (minimum 2 decimal places).

In persistence:

- Monetary values MUST be stored using fixed-precision numeric types.
- SQLite storage MUST preserve decimal precision.

In API contracts:

- Monetary values MUST be serialized without floating-point conversion.
- Loss of precision is forbidden.

---

### Percentages

Percentages SHALL be represented as `Decimal` values in the range [0, 100] across all layers:

- Domain
- Persistence
- API
- Events

Example:

- 21% → `21`
- 3.5% → `3.5`

Fractional representation in the range [0, 1] is strictly forbidden as a persistent or domain model representation.

If fractional computation is required for calculations (e.g., amount × percentage / 100), conversion MAY occur locally within a calculation expression, but the fractional value MUST NOT be:

- Stored
- Exposed via API
- Persisted
- Propagated across layers

Percentages MUST be modeled as an explicit domain type (e.g., `Percentage`) to prevent misuse.

---

### Rounding Rules

- Rounding MUST be explicit and deterministic.
- The rounding mode MUST be explicitly defined in calculation contexts.
- Implicit rounding behavior is forbidden.
- Financial calculations MUST document their rounding policy.

---

## Domain Modeling Rules

- Money and Percentage MUST be modeled as value objects.
- Raw Decimal usage for monetary logic SHOULD be avoided outside value objects.
- Arithmetic operations MUST preserve precision and invariants.

---

## Alternatives Considered

### 1. Floating Point Representation

Rejected because:
- Precision errors.
- Financial inconsistency risk.
- Non-deterministic behavior.

### 2. Fractional Percentages (0–1 Internal)

Rejected because:
- Contradicts Constitution.
- Increases risk of accidental double conversion.
- Reduces cognitive alignment with legal and business documents.

### 3. Store Money as Integer Cents

Rejected because:
- Complicates percentage and tax calculations.
- Reduces clarity of financial expressions.
- Adds unnecessary conversion overhead.

---

## Consequences

### Positive

- Financial determinism.
- Clear and uniform percentage semantics.
- Alignment with legal/business representations.
- No hidden numeric transformations.

### Negative / Trade-offs

- Requires explicit division by 100 in calculations.
- Slightly more verbose arithmetic.
- Strict discipline required in value object design.

---

## Operational Impact

- Database schema must use numeric types compatible with Decimal.
- Migration scripts must preserve precision.
- API serialization must avoid float conversion.
- Contract tests must validate percentage range constraints.

---

## Verification

Compliance is validated by:

- Unit tests verifying monetary precision.
- Static checks preventing float usage in domain.
- Tests validating percentage range [0, 100].
- Contract tests ensuring percentage schema stability.
- Code review enforcing value object usage.

---

## Plan Enforcement

Any feature introducing:

- Monetary values
- Percentage fields
- Tax logic
- Ratio-based calculations

MUST:

- Use Decimal.
- Respect 0–100 percentage representation.
- Explicitly define rounding behavior.
- Avoid float usage entirely.

If fractional (0–1) percentages are persisted or exposed, the plan is invalid.