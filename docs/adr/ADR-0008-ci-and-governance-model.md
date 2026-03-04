# ADR-0008: CI Pipeline and Governance Model

## Status
Accepted

## Context

The system follows strict architectural and contract discipline (see ADR-0001 to ADR-0007).

To ensure long-term maintainability, reproducibility, and boundary enforcement, all architectural decisions must be automatically validated.

Manual discipline is insufficient.

The project uses GitHub as version control platform and must enforce:

- Architectural boundaries
- Contract compatibility
- Code quality
- Test completeness
- Docker build reproducibility

A formal CI and governance model is required.


## Decision

The project SHALL use **GitHub Actions** as the mandatory CI pipeline.

No change may be merged without a successful CI run.

---

## Mandatory CI Checks

The pipeline MUST include the following jobs:

### 1. Linting

- Code style validation (e.g., ruff/flake8).
- No unused imports.
- No forbidden cross-root imports.

### 2. Static Typing

- Type checking (e.g., mypy).
- Type errors MUST fail the build.

### 3. Unit Tests

- Domain tests MUST run without infrastructure dependencies.
- Application layer tests MUST run in isolation where possible.
- Coverage thresholds MAY be defined.

### 4. Integration Tests

- Database-backed tests using SQLite (in-memory).
- Transaction rollback behavior verification.
- Migration upgrade tests (see ADR-0003).

### 5. Contract Tests

- OpenAPI schema validation.
- Backward compatibility checks.
- CloudEvents schema validation.
- Cross-root consumer/provider validation.

Any breaking contract change MUST fail CI unless version increment rules are respected.

### 6. Docker Build

- All images MUST build successfully.
- Images MUST run as non-root.
- Compose configuration MUST be validated.

---

## Pull Request Governance

- A Pull Request template MUST exist in the repository.
- Every PR MUST:
  - Declare affected ADRs.
  - Declare whether changes are breaking.
  - Confirm contract compatibility.
- No direct commits to main branch are allowed.
- Code review is mandatory before merge.

---

## Architectural Enforcement

CI MUST detect:

- Cross-root imports.
- Domain importing infrastructure.
- Business logic inside HTTP adapters.
- Missing migration files for schema changes.
- Missing contract tests when API/events change.

Failure in any enforcement rule MUST block merge.

---

## Documentation Discipline

- ADR changes MUST occur via new ADR files (no silent edits).
- Superseded ADRs MUST reference replacement ADR.
- Plans MUST reference applicable ADRs.

---

## Alternatives Considered

### 1. Manual Code Review Only

Rejected because:
- Not scalable.
- Prone to human error.
- Does not guarantee architectural integrity.

### 2. Local-Only Testing

Rejected because:
- Not reproducible.
- Allows environment drift.
- Violates deterministic build goals.

### 3. Separate CI per Root Without Integration Checks

Rejected because:
- Does not validate cross-root contracts.
- Weakens integration guarantees.

---

## Consequences

### Positive

- Architecture becomes enforceable.
- Contract discipline is automated.
- Safer refactoring.
- Reduced regression risk.
- Deterministic builds.

### Negative / Trade-offs

- CI complexity increases.
- Slower feedback loop compared to no validation.
- Maintenance effort for pipeline.

### Operational Impact

- Contributors must run tests locally before pushing.
- CI failures block merges.
- Pipeline configuration must be maintained as code.

---

## Verification

Compliance is validated by:

- Required status checks before merge.
- CI logs and artifacts.
- Periodic validation of enforcement rules.
- Review of ADR reference discipline in PRs.

---

## Plan Enforcement

Any feature implementation plan MUST:

- Define required tests (unit, integration, contract).
- Define whether migrations are needed.
- Define whether Docker changes are required.
- Explicitly reference affected ADRs.

If a plan omits governance requirements, it is invalid.