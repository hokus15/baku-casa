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

### Explicit Exception: Logging Framework Profiles (EN-0200)

As an explicit exception to centralized runtime configuration, logging framework profile
files MAY live as operational artifacts in the backend root (for example,
`backend/logging.dev.ini`, `backend/logging.test.ini`, `backend/logging.prod.ini`).

For this exception:

- The application MAY load the active logging framework profile directly at startup.
- The profile format and keys are framework-specific and are not required to be part of
  the typed centralized configuration schema.
- If the logging profile is missing or invalid, the application MAY apply a safe
  framework fallback and continue operating, while preserving the mandatory minimum
  logging baseline (timestamp UTC, level, service name, correlation_id, message).
- Fallback contract by environment (console output):
  - `dev`: human-friendly console output.
  - `test`: minimal human-friendly console output for deterministic assertions.
  - `prod`: structured JSON console output.
- This exception applies only to logging framework profiles and MUST NOT be generalized
  to other runtime configuration domains.

Observability guarantees for this exception are governed by ADR-0009.

## Consequences

### Positive

- Reproducible configuration across environments.
- Early failure on misconfiguration (safer deployments).
- Clear contract for configuration inputs (typed + validated).

### Negative

- Additional upfront structure for configuration definitions.
- Requires discipline to prevent ad-hoc configuration reads.

## Rules (Binding)

- All configuration access MUST go through the centralized configuration interface,
  except the explicit EN-0200 logging framework profile files described above.
- Modules MUST NOT read environment variables directly outside of the configuration system.
- Configuration keys MUST be stable and documented.
- Test configuration MUST be explicit and isolated from production settings.