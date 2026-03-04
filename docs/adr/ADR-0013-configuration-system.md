# ADR-0013: Configuration System (Typed, Centralized, Multi-Source)

## Status
Accepted

## Context

The system is self-hosted and deployed via Docker Compose (ADR-0007) with strict architectural boundaries (ADR-0002) and multi-root isolation (ADR-0001).

As the system evolves, configuration grows across multiple concerns (persistence, auth, logging, integrations). Without a centralized approach, configuration becomes:

- inconsistent across environments (dev/test/prod)
- hard to validate and reason about
- error-prone in deployment (missing/invalid values discovered late)

A unified configuration system is required to keep deployments reproducible and safe.

## Decision

The system SHALL implement a **typed, centralized configuration system**.

Configuration MUST:

- Be defined as a typed schema (explicit types and validation rules).
- Support multiple sources:
  - environment variables
  - configuration files
  - explicit defaults
- Apply a deterministic precedence order:
  1) environment variables
  2) configuration file
  3) defaults
- Be validated at application startup and MUST fail fast on:
  - missing required values
  - invalid values (type/range/format)
- Be environment-aware (dev/test/prod) without implicit conventions.

Secrets MUST NOT be baked into images (ADR-0007) and MUST be injectable at runtime.

The configuration system MUST NOT introduce dependencies into the Domain layer.

## Consequences

### Positive

- Reproducible configuration across environments.
- Early failure on misconfiguration (safer deployments).
- Clear contract for configuration inputs (typed + validated).

### Negative

- Additional upfront structure for configuration definitions.
- Requires discipline to prevent ad-hoc configuration reads.

## Rules (Binding)

- All configuration access MUST go through the centralized configuration interface.
- Modules MUST NOT read environment variables directly outside of the configuration system.
- Configuration keys MUST be stable and documented.
- Test configuration MUST be explicit and isolated from production settings.