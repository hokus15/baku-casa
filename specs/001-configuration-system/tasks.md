# Tasks: EN-0202 Configuration System

**Input**: Design documents from `/specs/001-configuration-system/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: TDD is mandatory for functional changes. Contract tests are not required in this item because external contract surfaces do not change.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Every task includes exact file paths

## Dependency Graph Issue

- None. `EN-0202` depends on `F-0001` (already `done`) and does not require later roadmap items.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare implementation workspace and shared artifacts for EN-0202

- [x] T001 Create EN-0202 implementation notes and key inventory in `specs/001-configuration-system/research.md`
- [x] T002 Create configuration package skeleton in `backend/src/baku/backend/application/configuration/__init__.py` and `backend/src/baku/backend/infrastructure/config/__init__.py`
- [x] T003 [P] Create configuration integration test package skeleton in `backend/tests/integration/configuration/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared configuration foundation required by all user stories

**CRITICAL**: No user story work starts before this phase is complete

- [x] T004 Define typed configuration models in `backend/src/baku/backend/application/configuration/models.py`
- [x] T005 Define typed configuration validation error codes in `backend/src/baku/backend/application/configuration/errors.py`
- [x] T006 Define centralized configuration provider port in `backend/src/baku/backend/application/configuration/provider_port.py`
- [x] T007 Implement source loaders for env/file/defaults in `backend/src/baku/backend/infrastructure/config/sources.py`
- [x] T008 Implement deterministic precedence resolver (`env > file > defaults`) in `backend/src/baku/backend/infrastructure/config/resolver.py`
- [x] T009 Implement startup validator with aggregated issues in `backend/src/baku/backend/infrastructure/config/validator.py`
- [x] T010 Wire centralized provider in composition root `backend/src/baku/backend/main.py` without introducing Domain dependencies

**Checkpoint**: Foundation ready for story implementation

---

## Phase 3: User Story 1 - Arranque con configuracion valida (Priority: P1) MVP

**Goal**: System starts successfully with valid required global configuration and deterministic source precedence.

**Independent Test**: Start backend with valid required keys and conflicting values across sources; verify successful startup and deterministic winner source.

### Tests for User Story 1

- [x] T011 [P] [US1] Add integration test for valid startup with required global keys in `backend/tests/integration/configuration/test_startup_valid_config.py`
- [x] T012 [P] [US1] Add integration test for deterministic precedence resolution in `backend/tests/integration/configuration/test_precedence_resolution.py`

### Implementation for User Story 1

- [x] T013 [US1] Implement resolved configuration profile assembly in `backend/src/baku/backend/infrastructure/config/runtime_settings.py`
- [x] T014 [US1] Refactor auth settings to consume centralized provider in `backend/src/baku/backend/infrastructure/config/auth_settings.py`
- [x] T015 [US1] Update auth policy adapter to use centralized settings access in `backend/src/baku/backend/infrastructure/config/auth_policy_provider.py`
- [x] T016 [US1] Ensure startup path loads and validates centralized configuration in `backend/src/baku/backend/main.py`

**Checkpoint**: US1 fully functional and independently testable

---

## Phase 4: User Story 2 - Fallo temprano ante configuracion invalida (Priority: P2)

**Goal**: Startup fails fast on invalid/missing required config and reports complete set of validation issues.

**Independent Test**: Start backend with multiple invalid/missing keys; verify startup failure and full aggregated validation report.

### Tests for User Story 2

- [x] T017 [P] [US2] Add integration test for fail-fast on missing required keys in `backend/tests/integration/configuration/test_missing_required_config.py`
- [x] T018 [P] [US2] Add integration test for aggregated validation errors in `backend/tests/integration/configuration/test_aggregated_validation_errors.py`

### Implementation for User Story 2

- [x] T019 [US2] Implement fail-fast startup behavior for invalid configuration in `backend/src/baku/backend/infrastructure/config/validator.py`
- [x] T020 [US2] Map configuration validation failures to typed application errors in `backend/src/baku/backend/application/configuration/errors.py`
- [x] T021 [US2] Ensure startup bootstrap aborts before functional router availability when config invalid in `backend/src/baku/backend/main.py`

**Checkpoint**: US2 fully functional and independently testable

---

## Phase 5: User Story 3 - Coherencia entre entornos y compatibilidad F-0001 (Priority: P3)

**Goal**: Keep reproducible behavior across `dev/test/prod`, emit warnings for undeclared keys, and preserve existing F-0001 auth configuration behavior.

**Independent Test**: Validate `dev/test/prod` resolution consistency, warning emission for undeclared keys, and no-regression for auth TTL/lockout behavior.

### Tests for User Story 3

- [x] T022 [P] [US3] Add integration test for undeclared keys warning without startup block in `backend/tests/integration/configuration/test_unknown_keys_warning.py`
- [x] T023 [P] [US3] Add integration test for test-profile isolation in `backend/tests/integration/configuration/test_test_profile_isolation.py`
- [x] T024 [P] [US3] Add auth compatibility regression tests for centralized configuration in `backend/tests/integration/auth/test_auth_config_compatibility.py`

### Implementation for User Story 3

- [x] T025 [US3] Implement warning emission path for undeclared configuration keys in `backend/src/baku/backend/infrastructure/config/validator.py`
- [x] T026 [US3] Implement environment profile selection and required-global-key policy in `backend/src/baku/backend/infrastructure/config/runtime_settings.py`
- [x] T027 [US3] Create explicit F-0001 auth configuration key inventory and legacy-to-centralized mapping in `specs/001-configuration-system/research.md`
- [x] T028 [US3] Adapt F-0001 auth settings consumption to centralized model in `backend/src/baku/backend/infrastructure/config/auth_settings.py` and `backend/src/baku/backend/infrastructure/config/auth_policy_provider.py`
- [x] T029 [US3] Update F-0001 composition wiring to consume centralized provider only in `backend/src/baku/backend/main.py`
- [x] T030 [US3] Preserve F-0001 semantics for token TTL and lockout policy through centralized config in `backend/src/baku/backend/application/auth/login_operator.py` and `backend/src/baku/backend/application/auth/token_validator.py`

**Checkpoint**: US3 fully functional and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, docs sync, and roadmap state synchronization

- [x] T031 [P] Update quickstart validation evidence for EN-0202 in `specs/001-configuration-system/quickstart.md`
- [x] T032 [P] Update operational configuration documentation in `README.md` and `backend/README.md`
- [x] T033 Run full backend quality gates (ruff, mypy, integration tests) and record results in `specs/001-configuration-system/plan.md`
- [x] T034 Update roadmap item status in `docs/spec/roadmap.md` when implementation enters/leaves execution (`planned` -> `in_progress` -> `done`)
- [x] T035 Update dependency graph status for `EN-0202` in `docs/spec/dependency-graph.yaml` in sync with roadmap status

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup): starts immediately
- Phase 2 (Foundational): depends on Phase 1
- Phase 3 (US1): depends on Phase 2
- Phase 4 (US2): depends on Phase 2 (can run after US1 starts, but independent)
- Phase 5 (US3): depends on Phase 2 and integrates with US1 outputs
- Phase 6 (Polish): depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: no dependency on other stories
- **US2 (P2)**: no functional dependency on US1
- **US3 (P3)**: depends on centralized config foundation and includes compatibility checks over F-0001 behavior

### Within Each User Story

- Tests first, must fail before implementation (TDD)
- Implementation after tests
- Story checkpoint before moving forward

## Parallel Opportunities

- T003 can run in parallel with T001-T002
- T011 and T012 can run in parallel
- T017 and T018 can run in parallel
- T022, T023, and T024 can run in parallel
- T028 and T029 can run in parallel

## Parallel Example: User Story 3

```bash
# Parallel test tasks for US3
T022 backend/tests/integration/configuration/test_unknown_keys_warning.py
T023 backend/tests/integration/configuration/test_test_profile_isolation.py
T024 backend/tests/integration/auth/test_auth_config_compatibility.py
```

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational phases
2. Deliver US1 (valid startup + deterministic precedence)
3. Validate US1 independently before expanding scope

### Incremental Delivery

1. US1: successful valid startup behavior
2. US2: fail-fast + aggregated validation errors
3. US3: environment consistency + warnings + F-0001 compatibility
4. Polish and documentation/state sync

### Team Parallelization

1. One stream on foundation (T004-T010)
2. One stream on US1 tests/implementation
3. One stream on US2 and US3 tests once foundation is stable

## Notes

- No contract versioning tasks are required for EN-0202 because there are no HTTP/event contract changes.
- Tasks avoid introducing new architectural decisions; they enforce existing ADR constraints.
