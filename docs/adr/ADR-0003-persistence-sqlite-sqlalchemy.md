# ADR-0003: Persistence Strategy (SQLite + SQLAlchemy + Migrations)

## Status
Accepted

## Context

The system is self-hosted and must run reliably on constrained hardware (e.g., Raspberry Pi) with minimal operational complexity.

Key drivers and constraints:

- No external services (e.g., Redis, PostgreSQL).
- Persistent storage is required starting from Feature 1, as the domain model is stateful from its initial definition.
- No in-memory-only implementation is allowed, even for early features.
- Accounting/ledger-like invariants require atomicity and consistency.
- The system must be reproducible and easy to back up/restore.
- The architecture enforces strict separation between Domain, ORM, and API models (see ADR-0002).

A persistence strategy must be defined that balances simplicity, reliability, portability, and correctness under concurrency.


## Decision

The system SHALL use:

- **SQLite** as the only database engine.
- **SQLAlchemy** as the ORM/data access library.
- A **versioned migration system** (e.g., Alembic or equivalent) as the only supported mechanism to evolve the schema.

### Data Model Separation (Binding)

- ORM models MUST be defined exclusively in the Infrastructure layer.
- Domain models MUST NOT import or depend on SQLAlchemy.
- Mapping between ORM ↔ Domain MUST be explicit.

### Transaction and Consistency Rules

- All state-changing use cases MUST execute within a single explicit database transaction.
- The transaction boundary MUST be owned by the Application layer (unit-of-work pattern) and implemented by Infrastructure.
- If a use case fails, the transaction MUST rollback fully (no partial commits).
- An in-memory persistence adapter MAY exist for isolated testing purposes only, but MUST NOT be used in production or integration environments.

### Concurrency and Locking Policy

- The system MUST assume concurrent access may occur (e.g., multiple HTTP requests).
- Conflicts MUST surface as explicit errors (typed conflict / 409 mapping at the API boundary).
- No unbounded silent retry loops are allowed.
- Writes MUST be designed to be safe under SQLite’s locking model (avoid long transactions; keep write transactions short).

### Migrations and Restorability

- Every schema change MUST be shipped as a migration.
- The repository MUST provide a deterministic way to:
  - create a fresh database from migrations
  - migrate an existing database forward to the latest schema
- Migrations MUST preserve restorability and data integrity.

### Backup and Restore Requirements

- The system MUST support offline backups by copying the SQLite database file.
- A backup/restore procedure MUST be documented and tested (at least one automated upgrade path test: backup → migrate → restore → integrity checks).

This decision is normative and binding.


## Alternatives Considered

### 1. PostgreSQL + SQLAlchemy

Rejected because:
- Adds operational overhead (service management, upgrades, resource usage).
- Conflicts with the “no external services” constraint and lightweight Raspberry Pi deployment goals.

### 2. SQLite + raw SQL (no ORM)

Rejected because:
- Increases implementation complexity and maintenance cost.
- Reduces consistency of access patterns and portability of implementations.
- ORM-independent Domain remains achievable with SQLAlchemy via explicit mapping.

### 3. SQLite without migrations (drop/recreate)

Rejected because:
- Breaks reproducibility for real user data.
- Makes upgrades unsafe and non-auditable.
- Violates the requirement for reproducible schema evolution.


## Consequences

### Positive

- Minimal operational footprint (single file database).
- Easy local development parity with production.
- Straightforward backup/restore model.
- ORM provides productivity while keeping Domain clean via explicit mapping.

### Negative / Trade-offs

- SQLite has write-lock constraints; careful transaction design is required.
- Horizontal scaling is limited.
- Some advanced DB features (row-level locks, rich concurrency) are not available.

### Operational Impact

- Deployments must manage the database file lifecycle (volume mounting, permissions).
- Upgrade procedures must apply migrations deterministically.
- Monitoring must include database file health and disk space.

### Verification

Compliance is validated by:

- Unit tests for Domain invariants without any DB.
- Integration tests ensuring each write use case is atomic (commit/rollback behavior).
- Migration tests: create-from-scratch and upgrade-from-previous-schema.
- Contract tests ensuring API semantics remain stable across schema upgrades.
- CI checks ensuring no SQLAlchemy imports in Domain/Application layers.


## Plan Enforcement

Any feature implementation plan MUST:

- Reference this ADR explicitly.
- Specify the transaction boundary for each write use case.
- Include required migrations for schema changes.
- Include or update the upgrade/restore verification tests when storage changes are introduced.

If a plan violates these rules, it is invalid.