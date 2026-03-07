# baku-casa Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-02

## Active Technologies
- Python 3.11 (roots `backend` y `bot`) + FastAPI (adapter HTTP), JWT stateless, pytest, mypy, ruff (001-acceso-autenticacion-operador)
- SQLite (estado de operador, versión de credencial, revocación por token actual, auditoría, bloqueo temporal) (001-acceso-autenticacion-operador)
- Python 3.11 + FastAPI, SQLAlchemy, PyJWT, bcrypt, python-dotenv (backend root) (001-configuration-system)
- SQLite (sin cambios de esquema para este item) (001-configuration-system)
- Python 3.11 + FastAPI, SQLAlchemy, PyJWT, bcrypt, python-dotenv, stdlib logging (001-logging-baseline-rotation)
- SQLite para datos de negocio (sin cambios de esquema); ficheros para logs operativos (001-logging-baseline-rotation)
- Python 3.11 + FastAPI, SQLAlchemy, pytest, tooling de calidad (`ruff`, `mypy`) (001-inmemory-db-testing)
- SQLite en memoria para pruebas de integración; SQLite persistente fuera del contexto de testing (001-inmemory-db-testing)

- Python 3.x por root (versionado exacto definido en cada `pyproject.toml`) + Tooling de lint, tipado y pruebas por root; GitHub Actions para CI (001-project-bootstrap)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.x por root (versionado exacto definido en cada `pyproject.toml`): Follow standard conventions

## Recent Changes
- 001-inmemory-db-testing: Added Python 3.11 + FastAPI, SQLAlchemy, pytest, tooling de calidad (`ruff`, `mypy`)
- 001-logging-baseline-rotation: Added Python 3.11 + FastAPI, SQLAlchemy, PyJWT, bcrypt, python-dotenv, stdlib logging
- 001-configuration-system: Added Python 3.11 + FastAPI, SQLAlchemy, PyJWT, bcrypt, python-dotenv (backend root)


<!-- MANUAL ADDITIONS START -->
# Manual Copilot Instructions – Baku.Casa

This project follows strict Spec Driven Development (SDD).

All generated code MUST comply with:


If a suggestion conflicts with any ADR, it MUST be considered invalid.

---

## Global Spec Integrity

The documents under `docs/spec/` define system intent.

If a change modifies:

- Business rules
- Domain terminology
- Invariants
- Feature scope
- Roadmap sequencing

The corresponding document under `docs/spec/` MUST be updated before implementation proceeds.

Code must never redefine global intent without updating the authoritative document.

---

## Architectural Constraints

### Monorepo Multi-root (ADR-0001)

- Never import across roots.
- Never suggest shared runtime packages.
- Integration MUST occur via versioned contracts only.
- Backend namespace: `baku.backend.*`
- Bot namespace: `baku.bot.*`

---

### Hexagonal Architecture (ADR-0002)

- Domain layer MUST be framework-independent.
- No SQLAlchemy, FastAPI, or infrastructure imports inside Domain.
- Business rules MUST NOT be placed in controllers.
- Explicit mapping between:
  - Domain models
  - ORM models
  - API DTOs

---

### Persistence (ADR-0003)

- SQLite is the only database.
- SQLAlchemy is used in Infrastructure only.
- All state-changing operations MUST be transactional.
- No in-memory persistence in production code.
- Migrations are mandatory for schema changes.

---

### API Discipline (ADR-0004)

- FastAPI is the HTTP adapter.
- Versioned path prefix: `/api/v{major}`.
- Pagination required for list endpoints.
- Stable DTOs within same MAJOR version.
- Typed error mapping to HTTP codes.

---

### Authentication (ADR-0005)

- Stateless JWT only.
- Token must include `ver` (credential_version).
- Password change must invalidate previous tokens.
- No server-side session store (no Redis).

---

### Contracts & Events (ADR-0006)

- All integration MUST be via versioned contracts.
- Events MUST use CloudEvents format.
- Breaking changes require MAJOR version increment.
- Contract tests are mandatory.

---

### Event Delivery (ADR-0010)

- Outbox pattern required.
- At-least-once delivery.
- Idempotency via CloudEvents `id`.
- No direct publish without persistence.

---

### Delivery Model (ADR-0007)

- All services containerized.
- No external managed services.
- MQTT optional via Docker Compose profile `events`.
- System must work without MQTT enabled.

---

### CI & Governance (ADR-0008)

- All code must pass lint, typing, tests.
- Contract tests required for API/event changes.
- No architectural violations.

---

### Error Model & Observability (ADR-0009)

- Typed errors only.
- Stable error codes (English).
- Spanish user messages.
- Structured logging.
- Correlation ID required.

---

## Code Generation Rules

When generating code:

- Prefer explicitness over magic.
- Avoid hidden framework coupling.
- Do not introduce global state.
- Do not introduce new infrastructure without ADR reference.
- Do not simplify by violating architectural boundaries.

---

## Testing Discipline

When generating tests:

- Domain tests must not require DB.
- Integration tests must use SQLite.
- Event publication must test outbox durability.
- JWT tests must validate revocation behavior.

---

## Forbidden Suggestions

Never suggest:

- Cross-root imports
- Shared internal packages
- Redis or external databases
- Removing versioning
- Mixing ORM models with domain logic
- Publishing events without outbox
- Storing business logic inside controllers

---

## When Unsure

If a feature appears to require:

- New infrastructure
- Breaking contract change
- Modification to persistence strategy
- Change in delivery semantics

The suggestion MUST explicitly state:
"Requires new ADR or ADR update."

---

The goal is architectural integrity, reproducibility, and long-term maintainability.
Shortcuts that violate ADRs are unacceptable.

## Documentation Synchronization Discipline (SDD)

This project follows Spec Driven Development.

Whenever a change modifies:

- Business behavior
- API contracts
- Event contracts
- Persistence model
- Error semantics
- Domain invariants

The corresponding specification in `specs/<feature>/` MUST be updated in the same Pull Request.

Rules:

- Code MUST NOT evolve ahead of the specification.
- If behavior changes, the spec MUST change first or in the same commit.
- If a contract changes, contract tests MUST be updated.
- If schema changes, migrations MUST be included.
- If a change affects architecture, a new ADR MUST be created or an ADR Gap declared.

Never implement behavioral changes without updating the related spec.
<!-- MANUAL ADDITIONS END -->
