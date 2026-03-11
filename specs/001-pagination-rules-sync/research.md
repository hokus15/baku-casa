# Phase 0 Research - Pagination Rules Sync (F-0001/F-0002/F-0003)

## Decision 1: Single transversal pagination policy across affected features

- Decision: All list/search collection surfaces in F-0001, F-0002, and F-0003 must be documented as mandatory pagination surfaces.
- Rationale: Aligns with ADR-0004 and avoids unbounded collections, preserving consistent user behavior.
- Alternatives considered:
  - Keep feature-specific pagination wording: rejected due to drift risk.
  - Apply policy only to F-0002/F-0003: rejected because F-0001 may expose collection endpoints over time.

## Decision 2: Centralized source of truth for defaults and limits

- Decision: Pagination defaults and maximum bounds are resolved only via EN-0202 configuration system.
- Rationale: EN-0202/ADR-0013 establish centralized, typed, deterministic configuration with explicit precedence.
- Alternatives considered:
  - Hardcoded defaults in each feature spec: rejected (non-governed and brittle).
  - Adapter-level local defaults: rejected (duplicates responsibility and contradicts EN-0202).

## Decision 3: Precedence model is fixed and explicit

- Decision: The precedence for pagination parameters is `environment variables > config file > defaults`.
- Rationale: This is the authoritative global precedence in EN-0202 and must remain stable across features.
- Alternatives considered:
  - `config file > environment variables`: rejected (contradicts EN-0202).
  - Environment-only configuration: rejected (insufficient flexibility for reproducible environments).

## Decision 4: Versioning and contract impact classification

- Decision: Treat this sync as non-breaking contract alignment unless endpoint shapes/semantics are changed.
- Rationale: Current scope is specification synchronization for already implemented features.
- Alternatives considered:
  - Immediate major bump: rejected because no planned incompatible contract change is introduced by this plan.

## Decision 5: Test strategy for safe rollout

- Decision: Use TDD coverage where behavior changes are required by implementation:
  - contract tests for collection shape/rules,
  - integration tests for pagination enforcement and precedence-driven behavior.
- Rationale: Satisfies constitutional quality gates and ADR-0008 governance.
- Alternatives considered:
  - Documentation-only validation without tests: rejected for functional behavior updates.

## Collection Surface Matrix

Inventario de todos los endpoints de coleccion expuestos por F-0001, F-0002 y F-0003:

| Feature | Endpoint | Tipo | Estado antes de sync | Accion requerida |
|---------|----------|------|----------------------|-----------------|
| F-0001 | (ninguno activo) | — | Sin coleccion en alcance | Solo declaracion documental preventiva |
| F-0002 | `GET /api/v1/owners` | lista + busqueda | Default 20 hardcoded en router; max 100 hardcoded en repo | Resolver default y max desde config (EN-0202) |
| F-0003 | `GET /api/v1/properties` | lista | Max desde config via `_get_pagination_defaults()`; default 20 hardcoded en router | Resolver default desde config (EN-0202) |
| F-0003 | `GET /api/v1/owners/{owner_id}/properties` | lista de propiedades del propietario | Max desde config; default 20 hardcoded en router | Resolver default desde config (EN-0202) |
| F-0003 | `GET /api/v1/properties/{property_id}/owners` | consulta de propietarios de una propiedad | Sin paginacion — coleccion acotada naturalmente | Fuera de alcance de este item (card. maxima baja) |

### Hallazgos clave

- El router de properties (`F-0003`) ya usa `_get_pagination_defaults()` para el maximo pero el default del Query sigue siendo hardcoded.
- El router de owners (`F-0002`) no usa `_get_pagination_defaults()` — ni para default ni para max.
- El repositorio SQLite de owners capura el maximo con `_MAX_PAGE_SIZE = 100` hardcoded, en lugar de recibirlo del router.
- La capa de configuracion (`runtime_settings.py`) ya tiene registradas las claves `pagination.default_page_size=20` y `pagination.max_page_size=100`.
- La alineacion correcta es: router resuelve `(default, max)` desde `RuntimeConfigurationProvider`; repositorio usa el valor ya capado que le pasa el router.

## Resolved Clarifications

- No unresolved `NEEDS CLARIFICATION` items remain.
- Dependency graph check confirms all required predecessors are already `done`.
- No ADR gap is required for this scope.
