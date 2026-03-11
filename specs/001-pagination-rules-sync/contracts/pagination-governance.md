# Contract: Pagination Governance for F-0001/F-0002/F-0003

## Contract Type

Behavioral contract for collection/list/search surfaces (HTTP-facing behavior expectations).

## Contract Rules

1. Collection/list/search surfaces MUST use mandatory pagination.
2. Pagination defaults and maximum bounds MUST be resolved exclusively from EN-0202 centralized configuration (`pagination.default_page_size`, `pagination.max_page_size`).
3. Resolution precedence MUST be:
   - `environment variables > config file > defaults`
4. Hardcoded pagination defaults/limits outside centralized configuration are forbidden. This applies equally to HTTP routers, application services, and repository layers.
5. Responses must remain bounded; unbounded collection responses are forbidden.
6. The cap (`min(requested_page_size, max_page_size)`) MUST be applied at the HTTP router layer BEFORE delegating to the application layer — repositories receive only already-capped values.

## Compatibility Classification

- Expected impact: non-breaking alignment.
- If any endpoint semantics or shape changes, compatibility must be reclassified and versioning rules from ADR-0004/ADR-0006 must be applied.

## Verification

- Contract tests validate mandatory pagination and bounded responses.
- Integration tests validate centralized precedence behavior.
- CI gates block merges on contract regressions.
