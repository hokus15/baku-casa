# Tasks: EN-0201 In-Memory Database Testing Baseline

**Input**: Design documents from `/specs/001-inmemory-db-testing/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: TDD is mandatory for functional changes in this enabler. New contract tests are not required because EN-0201 does not change HTTP/event contracts.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Every task includes exact file paths

## Dependency Graph Issue

- None. `EN-0201` depends on `EN-0202` (already `done`) and does not require later roadmap items.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare EN-0201 scaffolding for in-memory DB integration baseline in `backend/`

- [X] T001 Create persistence integration test package skeleton and scope conventions in `backend/tests/integration/persistence/__init__.py`
- [X] T002 [P] Add persistence integration test marker registration in `backend/pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared testing baseline required by all user stories

**CRITICAL**: No user story work starts before this phase is complete

- [X] T004 Implement explicit test DB override baseline in `backend/tests/conftest.py`
- [X] T005 Ensure in-memory engine semantics for test URL in `backend/src/baku/backend/infrastructure/persistence/sqlite/db.py`
- [X] T006 [P] Ensure deterministic migration bootstrap accepts in-memory URLs in `backend/src/baku/backend/infrastructure/persistence/sqlite/migrations.py`
- [X] T007 [P] Ensure runtime test settings reset coverage for DB profile isolation in `backend/src/baku/backend/infrastructure/config/runtime_settings.py`
- [X] T008 Add integration fixture documentation comments for isolation guarantees in `backend/tests/conftest.py`
- [X] T009 Confirm centralized config source behavior for explicit test DB URL precedence in `backend/src/baku/backend/infrastructure/config/sources.py`
- [X] T010 Add baseline wiring notes for persistence test mode in `backend/README.md`

**Checkpoint**: Foundation ready for user story implementation

---

## Phase 3: User Story 1 - Pruebas de integración aisladas (Priority: P1) MVP

**Goal**: Run integration tests with in-memory persistence and no external dependencies.

**Independent Test**: Execute persistence integration suite with explicit test profile and verify it runs against in-memory DB only.

### Tests for User Story 1

- [X] T011 [P] [US1] Add integration test for in-memory DB activation in `backend/tests/integration/persistence/test_inmemory_activation.py`
- [X] T012 [P] [US1] Add integration test for no external dependency execution in `backend/tests/integration/persistence/test_no_external_dependency.py`
- [X] T013 [P] [US1] Add integration test for per-test state isolation in `backend/tests/integration/persistence/test_state_isolation.py`

### Implementation for User Story 1

- [X] T014 [US1] Implement test-only in-memory URL activation in `backend/tests/conftest.py`
- [X] T015 [US1] Adjust engine/session behavior for shared in-memory lifecycle in `backend/src/baku/backend/infrastructure/persistence/sqlite/db.py`
- [X] T016 [US1] Ensure migrations execute correctly in in-memory test mode in `backend/src/baku/backend/infrastructure/persistence/sqlite/migrations.py`
- [X] T017 [US1] Add persistence integration test marker/classification conventions in `backend/tests/integration/persistence/__init__.py`

**Checkpoint**: US1 fully functional and independently testable

---

## Phase 4: User Story 2 - Esquema determinista para tests (Priority: P2)

**Goal**: Guarantee deterministic schema initialization for DB integration tests.

**Independent Test**: Re-run schema-dependent integration tests in clean contexts and confirm deterministic structure and outcomes.

### Tests for User Story 2

- [X] T018 [P] [US2] Add integration test for deterministic schema bootstrap in `backend/tests/integration/persistence/test_schema_bootstrap_determinism.py`
- [X] T019 [P] [US2] Add integration test for repeated clean execution consistency in `backend/tests/integration/persistence/test_repeated_execution_consistency.py`

### Implementation for User Story 2

- [X] T020 [US2] Implement deterministic schema setup sequence in shared fixtures in `backend/tests/conftest.py`
- [X] T021 [US2] Align migration bootstrap path resolution for deterministic test setup in `backend/src/baku/backend/infrastructure/persistence/sqlite/migrations.py`
- [X] T022 [US2] Ensure test setup does not leak schema state across tests in `backend/tests/conftest.py`

**Checkpoint**: US2 fully functional and independently testable

---

## Phase 5: User Story 3 - Configuración de testing segura y separada (Priority: P3)

**Goal**: Keep testing DB configuration explicit, isolated, and non-ambiguous versus runtime.

**Independent Test**: Verify runtime normal mode does not use in-memory test DB while test mode does.

### Tests for User Story 3

- [X] T023 [P] [US3] Add integration test for explicit test profile activation in `backend/tests/integration/configuration/test_persistence_test_profile_activation.py`
- [X] T024 [P] [US3] Add integration test for runtime non-testing isolation in `backend/tests/integration/configuration/test_runtime_db_profile_isolation.py`
- [X] T025 [P] [US3] Add integration test for config precedence of test DB URL in `backend/tests/integration/configuration/test_test_db_url_precedence.py`

### Implementation for User Story 3

- [X] T026 [US3] Implement explicit test-profile DB configuration flow in `backend/tests/conftest.py`
- [X] T027 [US3] Ensure runtime configuration reset behavior prevents stale profile reuse in `backend/src/baku/backend/infrastructure/config/runtime_settings.py`
- [X] T028 [US3] Align config source mapping documentation for test DB URL in `backend/src/baku/backend/infrastructure/config/sources.py`

**Checkpoint**: US3 fully functional and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, docs sync, and roadmap state consistency

- [X] T029 [P] Update EN-0201 operational/testing guidance in `specs/001-inmemory-db-testing/quickstart.md`
- [X] T030 [P] Update testing baseline documentation in `backend/README.md` and `README.md`
- [X] T031 [P] Synchronize feature docs impacted by EN-0201 baseline in `docs/spec/features/*.md`
- [X] T032 Run backend quality gates (`ruff`, `mypy`, `pytest`) and record evidence in `specs/001-inmemory-db-testing/plan.md`
- [X] T033 Run contract regression suite to confirm no external surface changes in `backend/tests/contract/auth/test_bootstrap_contract.py`, `backend/tests/contract/auth/test_login_logout_contract.py`, and `backend/tests/contract/auth/test_password_change_contract.py`
- [X] T034 Update EN-0201 status transitions in `docs/spec/roadmap.md` (`planned` -> `in_progress` -> `done`) aligned with implementation progress
- [X] T035 Update `EN-0201` status in `docs/spec/dependency-graph.yaml` aligned with roadmap status

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup): starts immediately
- Phase 2 (Foundational): depends on Phase 1 and blocks all user stories
- Phase 3 (US1): depends on Phase 2
- Phase 4 (US2): depends on Phase 2 and uses US1 fixture baseline
- Phase 5 (US3): depends on Phase 2 and reuses shared config/runtime baseline
- Phase 6 (Polish): depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: no dependency on other stories
- **US2 (P2)**: depends on foundational fixture/migration baseline
- **US3 (P3)**: depends on foundational config baseline

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
- Foundation: T006 and T007 can run in parallel after T004/T005
- US1: T011/T012/T013 can run in parallel
- US2: T018 and T019 can run in parallel
- US3: T023/T024/T025 can run in parallel
- Polish: T029/T030/T031 can run in parallel

## Parallel Example: User Story 1

```bash
# Parallel tests for US1
T011 backend/tests/integration/persistence/test_inmemory_activation.py
T012 backend/tests/integration/persistence/test_no_external_dependency.py
T013 backend/tests/integration/persistence/test_state_isolation.py
```

## Parallel Example: User Story 2

```bash
# Parallel tests for US2
T018 backend/tests/integration/persistence/test_schema_bootstrap_determinism.py
T019 backend/tests/integration/persistence/test_repeated_execution_consistency.py
```

## Parallel Example: User Story 3

```bash
# Parallel tests for US3
T023 backend/tests/integration/configuration/test_persistence_test_profile_activation.py
T024 backend/tests/integration/configuration/test_runtime_db_profile_isolation.py
T025 backend/tests/integration/configuration/test_test_db_url_precedence.py
```

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Setup (Phase 1)
2. Complete Foundational (Phase 2)
3. Complete US1 (Phase 3)
4. Validate US1 independently before widening scope

### Incremental Delivery

1. Deliver US1 (in-memory isolated integration execution)
2. Deliver US2 (deterministic schema bootstrap)
3. Deliver US3 (explicit and isolated test configuration)
4. Execute Polish phase and documentation/state synchronization

### Parallel Team Strategy

1. One stream on shared fixtures and persistence bootstrap (`conftest.py`, `db.py`, `migrations.py`)
2. One stream on persistence integration tests under `backend/tests/integration/persistence/`
3. One stream on configuration isolation tests under `backend/tests/integration/configuration/`

## Notes

- No ADR modifications are required for EN-0201 implementation.
- No new contract surfaces are introduced; existing contract tests remain regression guards.
- Tasks intentionally avoid migrations generation and implementation-specific code output.
