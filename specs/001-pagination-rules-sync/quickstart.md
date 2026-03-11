# Quickstart - Pagination Rules Sync (F-0001/F-0002/F-0003)

## Objective

Validate that list/search behaviors for F-0001, F-0002, and F-0003 are aligned with EN-0202 pagination governance.

## 1. Update feature specs

- Ensure the following docs explicitly state mandatory pagination and centralized EN-0202 resolution with fixed precedence:
  - `docs/spec/features/F-0001-acceso-y-autenticacion-operador.md`
  - `docs/spec/features/F-0002-propietarios-sujetos-fiscales.md`
  - `docs/spec/features/F-0003-propiedades-y-titularidad.md`

## 2. Validate contract expectations

- Confirm collection/list/search surfaces are bounded and governed by centralized defaults/limits.
- Confirm no hardcoded pagination defaults/limits are introduced outside central configuration.

## 3. Verify EN-0202 precedence behavior

**Goal**: confirm that `environment variables > config file > defaults` is enforced for pagination parameters in all collection surfaces.

### 3.1 Default page_size resolution

```sh
# Should return page_size = 5 (not the built-in default of 20)
AUTH_JWT_SECRET=test PAGINATION_DEFAULT_PAGE_SIZE=5 pytest backend/tests/contract/test_no_hardcoded_pagination_defaults.py -v
```

Expected outcome: all owners and properties list endpoints use `page_size=5` when no page_size query param is supplied.

### 3.2 Max page_size enforcement

```sh
# Request page_size=100 but config limits it to 3
AUTH_JWT_SECRET=test PAGINATION_MAX_PAGE_SIZE=3 pytest backend/tests/integration/test_pagination_limits_from_configuration.py -v
```

Expected outcome: responses for list endpoints never return more than 3 items per page regardless of the requested `page_size`.

### 3.3 file > defaults precedence

Create a temporary `.env` file with `PAGINATION_DEFAULT_PAGE_SIZE=7` and run:

```sh
pytest backend/tests/integration/test_pagination_precedence_en0202.py -v
```

Expected outcome: file-sourced value (7) overrides the built-in default (20).

### 3.4 env > file precedence

Set both `PAGINATION_DEFAULT_PAGE_SIZE=5` (env) and a `.env` file with `PAGINATION_DEFAULT_PAGE_SIZE=7`:

Expected outcome: env-sourced value (5) wins.

## 4. Execute quality gates

- Run lint and type checks.
- Run integration tests for affected collection endpoints.
- Run contract tests for collection behavior and compatibility.

## 5. Verify roadmap consistency

- Confirm no status changes are introduced for F-0001, F-0002, F-0003.
- Confirm `docs/roadmap.md` and `docs/dependency-graph.yaml` remain consistent.

## Expected Result

All affected feature specs and tests confirm one synchronized pagination policy, with deterministic EN-0202 precedence and no hardcoded overrides.
