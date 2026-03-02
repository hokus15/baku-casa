# ADR-0002: Hexagonal Architecture (Ports and Adapters)

## Status
Accepted

## Context

The system manages financial operations (accruals, payments, reversals, ledger integrity) with strict accounting invariants defined in the Constitution.

The architecture must ensure:

- Business logic remains independent from frameworks
- Domain rules are testable in isolation
- Infrastructure can evolve without affecting core logic
- Strong separation between:
  - Domain model
  - Persistence model (ORM)
  - API model (DTO)

The system must also remain reproducible and portable across implementations, as mandated by Spec Driven Development.

A clear architectural style is required to enforce these boundaries.


## Decision

The system SHALL adopt a **Hexagonal Architecture (Ports and Adapters)** with strict separation of layers and dependency direction.

### Layer Model

The backend SHALL be structured into the following logical layers:

1. **Domain**
   - Pure business logic
   - No framework imports
   - No ORM dependencies
   - No HTTP dependencies
   - Contains entities, value objects, domain services, and invariants

2. **Application**
   - Orchestrates use cases
   - Depends on Domain
   - Defines ports (interfaces) for external dependencies
   - No framework-specific logic

3. **Infrastructure**
   - Implements persistence, external services, integrations
   - Implements ports defined in Application
   - May depend on frameworks (e.g., SQLAlchemy)

4. **Interfaces (Adapters)**
   - HTTP controllers (FastAPI)
   - CLI, Bot, or other entry points
   - Responsible for DTO mapping
   - No business rules allowed

### Dependency Direction

Dependencies MUST follow this direction:

Interfaces → Application → Domain  
Infrastructure → Application  
Domain MUST NOT depend on any other layer.

### Model Separation

The following models MUST be strictly separated:

- Domain Models
- ORM Models
- API DTOs

Mapping between them MUST be explicit and implemented in adapters or infrastructure.

No model may serve multiple architectural layers.

### Invariants

All accounting and business invariants MUST be enforced in the Domain layer.

Adapters and controllers MUST NOT contain business logic.

This decision is normative and binding.


## Alternatives Considered

### 1. Layered Architecture (Traditional MVC)

Rejected because:
- Encourages leakage of business logic into controllers.
- Weakens domain isolation.
- Makes invariant enforcement harder to audit.

### 2. Active Record Pattern

Rejected because:
- Couples domain logic to ORM.
- Prevents pure domain testing.
- Violates separation between persistence and business logic.

### 3. Framework-Centric Architecture

Rejected because:
- Ties core logic to FastAPI/SQLAlchemy.
- Reduces portability.
- Breaks reproducibility across implementations.


## Consequences

### Positive

- Strong domain isolation
- Testable business logic without infrastructure
- Clear dependency boundaries
- Easier long-term maintainability
- Safer refactoring of infrastructure

### Negative / Trade-offs

- Requires explicit mapping between models.
- Introduces additional structural complexity.
- Higher initial design effort.

### Operational Impact

- Clear module structure required inside backend.
- Developers must respect dependency direction.
- Code reviews must enforce boundary rules.

### Verification

Compliance is validated by:

- Static analysis preventing forbidden imports.
- Unit tests covering Domain in isolation.
- Code review ensuring no business logic in adapters.
- CI checks enforcing architectural boundaries.


## Plan Enforcement

Any feature implementation plan MUST:

- Place business rules exclusively in the Domain layer.
- Define ports in the Application layer for external dependencies.
- Implement infrastructure details outside Domain.
- Avoid mixing ORM or HTTP concerns with business logic.

If a plan violates these rules, it is invalid.