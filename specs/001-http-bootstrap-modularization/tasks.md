# Tasks: EN-0300 HTTP Application Bootstrap Modularization

**Input**: Design documents from `/specs/001-http-bootstrap-modularization/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: TDD is mandatory for this enabler (red -> green -> refactor). New contract tests are not required because EN-0300 does not change HTTP/event contracts; contract regression remains required.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Every task includes exact file paths

## Dependency Graph Issue

- None. `EN-0300` depends on `EN-0202` (`done`) and does not require later roadmap items.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare EN-0300 scaffolding for HTTP bootstrap modularization in `backend/`.

- [X] T001 Create bootstrap integration test package skeleton in `backend/tests/integration/bootstrap/__init__.py`
- [X] T002 [P] Register bootstrap integration marker in `backend/pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish bootstrap module boundaries required by all user stories.

**CRITICAL**: No user story work starts before this phase is complete.

- [X] T003 Create bootstrap module package in `backend/src/baku/backend/interfaces/http/bootstrap/__init__.py`
- [X] T004 Define bootstrap boundary contracts in `backend/src/baku/backend/interfaces/http/bootstrap/contracts.py`
- [X] T005 [P] Add app factory orchestration scaffold in `backend/src/baku/backend/interfaces/http/bootstrap/app_factory.py`
- [X] T006 [P] Add lifespan bootstrap scaffold in `backend/src/baku/backend/interfaces/http/bootstrap/lifespan.py`
- [X] T007 [P] Add dependency wiring scaffold in `backend/src/baku/backend/interfaces/http/bootstrap/dependency_wiring.py`
- [X] T008 [P] Add middleware registry scaffold in `backend/src/baku/backend/interfaces/http/bootstrap/middleware_registry.py`
- [X] T009 [P] Add error handler registry scaffold in `backend/src/baku/backend/interfaces/http/bootstrap/error_handlers_registry.py`
- [X] T010 [P] Add router registry scaffold in `backend/src/baku/backend/interfaces/http/bootstrap/router_registry.py`
- [X] T011 Keep `main.py` as thin entrypoint delegating bootstrap concerns in `backend/src/baku/backend/main.py`
- [X] T012 Add foundational bootstrap wiring contract (scope, boundaries, inventory base) in `backend/README.md`

**Checkpoint**: Foundation ready for user story implementation.

---

## Phase 3: User Story 1 - Bootstrap con responsabilidades separadas (Priority: P1) MVP

**Goal**: Entry point remains bounded while bootstrap responsibilities are separated into traceable components.

**Independent Test**: Run bootstrap integration tests to confirm `main.py` no longer concentrates heterogeneous startup responsibilities and behavior remains equivalent.

### Tests for User Story 1

- [X] T013 [P] [US1] Add integration test for thin HTTP entrypoint boundary in `backend/tests/integration/bootstrap/test_entrypoint_boundaries.py`
- [X] T014 [P] [US1] Add integration test for bootstrap responsibility separation in `backend/tests/integration/bootstrap/test_bootstrap_responsibility_separation.py`

### Implementation for User Story 1

- [X] T015 [US1] Implement app creation orchestration in `backend/src/baku/backend/interfaces/http/bootstrap/app_factory.py`
- [X] T016 [US1] Implement bootstrap lifecycle delegation in `backend/src/baku/backend/interfaces/http/bootstrap/lifespan.py`
- [X] T017 [US1] Refactor entrypoint to delegate startup responsibilities in `backend/src/baku/backend/main.py`
- [X] T018 [US1] Finalize bootstrap module exports for traceability in `backend/src/baku/backend/interfaces/http/bootstrap/__init__.py`

**Checkpoint**: US1 fully functional and independently testable.

---

## Phase 4: User Story 2 - Composition root unico para dependencias entre capas (Priority: P2)

**Goal**: Keep dependency composition centralized in a single composition root while preserving hexagonal boundaries.

**Independent Test**: Run architecture/integration tests to verify no new composition points appear outside the designated wiring module.

### Tests for User Story 2

- [X] T019 [P] [US2] Add integration test for single composition root enforcement in `backend/tests/integration/bootstrap/test_single_composition_root.py`
- [X] T020 [P] [US2] Add integration test for dependency override equivalence in `backend/tests/integration/bootstrap/test_dependency_wiring_equivalence.py`

### Implementation for User Story 2

- [X] T021 [US2] Consolidate dependency override mapping in `backend/src/baku/backend/interfaces/http/bootstrap/dependency_wiring.py`
- [X] T022 [US2] Centralize middleware registration via registry module in `backend/src/baku/backend/interfaces/http/bootstrap/middleware_registry.py`
- [X] T023 [US2] Centralize error handler registration via registry module in `backend/src/baku/backend/interfaces/http/bootstrap/error_handlers_registry.py`
- [X] T024 [US2] Centralize router registration via registry module in `backend/src/baku/backend/interfaces/http/bootstrap/router_registry.py`

**Checkpoint**: US2 fully functional and independently testable.

---

## Phase 5: User Story 3 - Evolucion del bootstrap sin impacto funcional externo (Priority: P3)

**Goal**: Preserve external HTTP behavior and fail-fast startup semantics while completing structural modularization.

**Independent Test**: Run fail-fast startup tests plus functional/contract regression to confirm no external contract drift.

### Tests for User Story 3

- [X] T025 [P] [US3] Add integration test for fail-fast bootstrap critical errors in `backend/tests/integration/bootstrap/test_fail_fast_bootstrap_errors.py`
- [X] T026 [P] [US3] Add integration test for unchanged HTTP surface sentinel in `backend/tests/integration/bootstrap/test_http_surface_unchanged.py`
- [X] T037 [P] [US3] Add integration test for bootstrap error traceability (structured error/correlation evidence) in `backend/tests/integration/bootstrap/test_bootstrap_error_traceability.py`

### Implementation for User Story 3

- [X] T027 [US3] Preserve explicit fail-fast behavior in bootstrap lifecycle in `backend/src/baku/backend/interfaces/http/bootstrap/lifespan.py`
- [X] T028 [US3] Preserve startup functional equivalence in thin entrypoint integration in `backend/src/baku/backend/main.py`
- [X] T029 [US3] Align quickstart validation for fail-fast and no-contract-change checks in `specs/001-http-bootstrap-modularization/quickstart.md`

**Checkpoint**: US3 fully functional and independently testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final quality validation, documentation sync, and roadmap state consistency.

- [X] T030 [P] Update final EN-0300 operational notes and validation evidence in `backend/README.md` (post-implementation/polish scope)
- [X] T031 [P] Update EN-0300 roadmap baseline mention in `README.md`
- [X] T032 [P] Synchronize feature docs only if EN-0300 dependencies become explicit in `docs/spec/features/*.md`
- [X] T033 Run backend quality gates (`ruff`, `mypy`, `pytest`) and record evidence in `specs/001-http-bootstrap-modularization/plan.md`
- [X] T034 Run contract regression suite in `backend/tests/contract/auth/test_bootstrap_contract.py`, `backend/tests/contract/auth/test_login_logout_contract.py`, and `backend/tests/contract/auth/test_password_change_contract.py`
- [X] T035 Update EN-0300 status transitions in `docs/spec/roadmap.md` (`planned` -> `in_progress` -> `done`) aligned with implementation progress
- [X] T036 Update EN-0300 status in `docs/spec/dependency-graph.yaml` aligned with roadmap status

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup): starts immediately
- Phase 2 (Foundational): depends on Phase 1 and blocks all user stories
- Phase 3 (US1): depends on Phase 2
- Phase 4 (US2): depends on Phase 2 and uses US1 bootstrap boundaries
- Phase 5 (US3): depends on Phase 2 and reuses shared bootstrap modules
- Phase 6 (Polish): depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: no dependency on other stories
- **US2 (P2)**: depends on foundational bootstrap module boundaries
- **US3 (P3)**: depends on foundational bootstrap module boundaries and uses US1/US2 structure

### Within Each User Story

- Write tests first and confirm failing behavior (TDD)
- Implement minimal code to pass tests
- Refactor while preserving green tests
- Complete story checkpoint before moving to next priority

### Dependency Graph

- Foundation -> US1
- Foundation -> US2
- Foundation -> US3
- US1 + US2 + US3 -> Polish

## Parallel Opportunities

- Setup: T001 and T002 can run in parallel
- Foundation: T005, T006, T007, T008, T009, and T010 can run in parallel after T003/T004
- US1: T013 and T014 can run in parallel
- US2: T019 and T020 can run in parallel
- US3: T025, T026, and T037 can run in parallel
- Polish: T030, T031, and T032 can run in parallel

## Parallel Example: User Story 1

```bash
# Parallel tests for US1
T013 backend/tests/integration/bootstrap/test_entrypoint_boundaries.py
T014 backend/tests/integration/bootstrap/test_bootstrap_responsibility_separation.py
```

## Parallel Example: User Story 2

```bash
# Parallel tests for US2
T019 backend/tests/integration/bootstrap/test_single_composition_root.py
T020 backend/tests/integration/bootstrap/test_dependency_wiring_equivalence.py
```

## Parallel Example: User Story 3

```bash
# Parallel tests for US3
T025 backend/tests/integration/bootstrap/test_fail_fast_bootstrap_errors.py
T026 backend/tests/integration/bootstrap/test_http_surface_unchanged.py
T037 backend/tests/integration/bootstrap/test_bootstrap_error_traceability.py
```

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Setup (Phase 1)
2. Complete Foundational (Phase 2)
3. Complete US1 (Phase 3)
4. Validate US1 independently before widening scope

### Incremental Delivery

1. Deliver US1 (bootstrap responsibility separation)
2. Deliver US2 (single composition root enforcement)
3. Deliver US3 (fail-fast + no external drift)
4. Execute Polish phase and documentation/state synchronization

### Parallel Team Strategy

1. One stream on bootstrap module boundaries and entrypoint delegation (`main.py`, `interfaces/http/bootstrap/`)
2. One stream on bootstrap integration tests under `backend/tests/integration/bootstrap/`
3. One stream on quality/contract regression and documentation synchronization

## Notes

- No ADR modifications are required for EN-0300 implementation.
- No contract surface changes are introduced; contract tests remain regression guards.
- Tasks avoid code snippets and focus on executable work units mapped to concrete files.
