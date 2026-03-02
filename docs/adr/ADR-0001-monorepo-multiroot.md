# ADR-0001: Monorepo Multi-root Architecture

## Status
Accepted

## Context

The system is a self-hosted rental management platform designed to run on lightweight infrastructure (e.g., Raspberry Pi).  
It consists of multiple independently deployable components:

- Backend (core domain + HTTP API)
- Bot (Telegram interface)
- Potential future components (e.g., frontend)

The Constitution enforces:

- Strict modular boundaries
- Hexagonal architecture
- Reproducible builds
- No implicit coupling
- Contract-based integration

A structural repository decision is required to:

- Prevent accidental runtime coupling
- Enforce explicit integration contracts
- Allow independent evolution of components
- Preserve architectural integrity over time
- Keep the system maintainable under constrained hardware


## Decision

The system SHALL adopt a **monorepo multi-root architecture** with the following binding rules:

### Repository Structure

1. The repository root SHALL contain independent top-level directories:
   - `backend/`
   - `bot/`
   - Additional roots MAY be added in the future (e.g., `frontend/`).

2. The repository root MUST contain:
   - A top-level `README.md`
   - A `docker/` directory containing Docker Compose definitions

### Root-Level Requirements

Each root:

- MUST have its own `pyproject.toml`
- MUST manage its own dependency graph
- MUST contain:
  - `src/`
  - `tests/`
  - `README.md`
- MUST define its own Python namespace

### Namespace Convention

- Backend modules MUST use: `baku.backend.*`
- Bot modules MUST use: `baku.bot.*`

### Isolation Rules

- Runtime shared code between roots is strictly forbidden.
- No root may directly import another root.
- Integration between roots MUST occur exclusively via:
  - Explicit, versioned contracts (e.g., HTTP/OpenAPI)
  - Mandatory contract tests validating compatibility

### Integration Discipline

- Contracts MUST be versioned.
- Breaking changes require a major version increment.
- Contract tests MUST run in CI.

This decision is normative and binding.


## Alternatives Considered

### 1. Single-Package Monolith

All components inside a single Python package.

Rejected because:
- Encourages tight coupling.
- Weakens contract enforcement.
- Reduces independent deployability.
- Makes boundary violations harder to detect.

### 2. Polyrepo (One Repository per Component)

Each component in its own repository.

Rejected because:
- Adds operational overhead.
- Makes coordinated changes harder.
- Slows development for a small team/project.

### 3. Shared Internal Library Between Roots

Common runtime package imported by all components.

Rejected because:
- Creates implicit coupling.
- Breaks isolation guarantees.
- Encourages leakage of domain logic across boundaries.


## Consequences

### Positive

- Strong architectural boundaries
- Enforced contract discipline
- Independent evolution of components
- Clean deployment separation
- Reduced risk of accidental coupling

### Negative / Trade-offs

- Some duplication may occur across roots.
- Contract tests introduce additional maintenance effort.
- Strict isolation increases short-term friction.

### Operational Impact

- Docker images are built per root.
- CI must validate each root independently.
- Contract tests must run across components.

### Verification

Compliance is validated by:

- CI checks preventing cross-root imports.
- Contract tests verifying integration compatibility.
- Code review enforcing namespace rules.
- Independent dependency resolution per root.


## Plan Enforcement

Any feature implementation plan MUST:

- Explicitly acknowledge this ADR.
- Avoid introducing cross-root runtime imports.
- Define integration exclusively through versioned contracts.

If a plan violates these rules, it is invalid.