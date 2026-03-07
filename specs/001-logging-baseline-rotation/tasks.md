# Tasks: EN-0200 Application Logging Baseline with Daily Rotation

**Input**: Design documents from `/specs/001-logging-baseline-rotation/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: TDD is mandatory for functional changes in this enabler. Contract versioning tests are not added because external contracts do not change.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Every task includes exact file paths

## Dependency Graph Issue

- None. `EN-0200` depends on `EN-0202` (already `done`) and does not require later roadmap items.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare EN-0200 scaffolding for standard framework-based logging with external config files at backend root

- [X] T001 Create logging infrastructure package skeleton in `backend/src/baku/backend/infrastructure/logging/__init__.py`
- [X] T002 [P] Create logging integration test package skeleton in `backend/tests/integration/logging/__init__.py`
- [X] T003 [P] Create framework-specific logging configuration files at backend root in `backend/logging.dev.ini`, `backend/logging.test.ini`, and `backend/logging.prod.ini`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build minimal logging integration so the app only loads framework config and uses logger APIs

**CRITICAL**: No user story work starts before this phase is complete

- [X] T004 Implement framework config loader that reads backend-root logging profile and calls `logging.config.fileConfig` in `backend/src/baku/backend/infrastructure/logging/bootstrap.py`
- [X] T005 Implement environment-to-profile resolver (`dev|test|prod` -> `logging.<env>.ini`) in `backend/src/baku/backend/infrastructure/logging/bootstrap.py`
- [X] T006 [P] Define dual formatter and dual handler sections (JSON + human) in `backend/logging.dev.ini`
- [X] T007 [P] Define dual formatter and dual handler sections (JSON + human) in `backend/logging.test.ini`
- [X] T008 Define dual formatter and dual handler sections (JSON + human) with production levels in `backend/logging.prod.ini`
- [X] T009 Configure `TimedRotatingFileHandler` sections (midnight Europe/Madrid, retention days) in `backend/logging.dev.ini`, `backend/logging.test.ini`, and `backend/logging.prod.ini`
- [X] T010 Configure root/app loggers and propagation policy in `backend/logging.dev.ini`, `backend/logging.test.ini`, and `backend/logging.prod.ini`
- [X] T011 Wire logging bootstrap in `backend/src/baku/backend/main.py` so application startup only loads framework config and, when profile is missing/invalid, applies explicit fallback behavior aligned with FR-008 and fallback console contract by environment (`dev` human-friendly, `test` human-friendly minimalista, `prod` JSON)

**Checkpoint**: Foundation ready for user story implementation

---

## Phase 3: User Story 1 - Diagnostico tecnico consistente (Priority: P1) MVP

**Goal**: Ensure relevant backend flows emit structured logs with required fields and safe content.

**Independent Test**: Execute auth flows (bootstrap/login/logout/password change) and verify required fields and sanitization in both log outputs.

### Tests for User Story 1

- [X] T012 [P] [US1] Add integration test for required structured logging fields in auth flow in `backend/tests/integration/logging/test_required_fields.py`
- [X] T013 [P] [US1] Add integration test for secret/token/password sanitization in logs in `backend/tests/integration/logging/test_sensitive_data_sanitization.py`
- [X] T041 [P] [US1] Add integration test asserting log messages remain in English and structured field keys use `snake_case` in `backend/tests/integration/logging/test_message_language_and_field_naming.py`
- [X] T042 [P] [US1] Add integration test asserting contextual key-value data is emitted as structured fields and not appended into `message` in `backend/tests/integration/logging/test_structured_context_fields.py`

### Implementation for User Story 1

- [X] T014 [P] [US1] Add structured log emission for bootstrap flow use case in `backend/src/baku/backend/application/auth/bootstrap_operator.py`
- [X] T015 [P] [US1] Add structured log emission for login/logout flow use cases in `backend/src/baku/backend/application/auth/login_operator.py` and `backend/src/baku/backend/application/auth/logout_operator.py`
- [X] T016 [P] [US1] Add structured log emission for password change flow in `backend/src/baku/backend/application/auth/change_operator_password.py`
- [X] T017 [US1] Add request lifecycle logging (start/end and failure path) in `backend/src/baku/backend/interfaces/http/api/v1/auth_router.py`
- [X] T018 [US1] Ensure typed error mapping emits safe structured diagnostic logs in `backend/src/baku/backend/interfaces/http/error_mapper.py`

**Checkpoint**: US1 fully functional and independently testable

---

## Phase 4: User Story 2 - Trazabilidad extremo a extremo con correlation_id (Priority: P2)

**Goal**: Preserve or generate `correlation_id` and propagate it across all logs of a request lifecycle.

**Independent Test**: Send requests with and without `X-Correlation-ID` and verify per-request consistency across emitted logs and response headers.

### Tests for User Story 2

- [X] T019 [P] [US2] Add integration test for incoming header correlation propagation in `backend/tests/integration/logging/test_correlation_propagation.py`
- [X] T020 [P] [US2] Add integration test for generated correlation id when header is absent in `backend/tests/integration/logging/test_correlation_generation.py`

### Implementation for User Story 2

- [X] T021 [US2] Expose correlation id accessor for infrastructure usage in `backend/src/baku/backend/interfaces/http/middleware/correlation_id.py`
- [X] T022 [US2] Implement logging context filter that injects `correlation_id` into all records in `backend/src/baku/backend/infrastructure/logging/context.py`
- [X] T023 [US2] Integrate correlation-aware filters into logging bootstrap in `backend/src/baku/backend/infrastructure/logging/bootstrap.py`
- [X] T024 [US2] Ensure middleware registration order preserves correlation context before handlers execute in `backend/src/baku/backend/main.py`

**Checkpoint**: US2 fully functional and independently testable

---

## Phase 5: User Story 3 - Rotacion diaria y retencion configurable por entorno (Priority: P3)

**Goal**: Keep rotation, retention, and dual output fully managed by framework config files at backend root.

**Independent Test**: Validate startup loading `logging.<env>.ini`, verify framework-only rotation/retention behavior, and confirm fallback writes to console per environment contract while app remains operational.

### Tests for User Story 3

- [X] T025 [P] [US3] Add integration test for startup with missing logging profile ensuring fallback preserves mandatory minimum baseline and writes to console in `backend/tests/integration/logging/test_missing_profile_fallback.py`
- [X] T026 [P] [US3] Add integration test for fallback console contract by environment (`dev` human-friendly, `test` human-friendly minimalista, `prod` JSON) in `backend/tests/integration/logging/test_env_profile_selection.py`
- [X] T027 [P] [US3] Add integration test for rotation/retention with continuity-integrity assertion (before/after rotation) proving no loss of relevant events in `backend/tests/integration/logging/test_rotation_retention_policy.py`

### Implementation for User Story 3

- [X] T028 [P] [US3] Finalize dev profile values (levels, file paths, retention days) in `backend/logging.dev.ini`
- [X] T029 [P] [US3] Finalize test profile values (levels, file paths, retention days) in `backend/logging.test.ini`
- [X] T030 [P] [US3] Finalize prod profile values (levels, file paths, retention days) in `backend/logging.prod.ini`
- [X] T031 [US3] Implement timezone-aware midnight rollover integration using framework handler settings in `backend/src/baku/backend/infrastructure/logging/bootstrap.py`
- [X] T032 [US3] Document and implement fallback console contract by environment when profile file is absent/invalid (no app crash) in `backend/src/baku/backend/infrastructure/logging/bootstrap.py`
- [X] T033 [US3] Validate two-output file generation (JSON + human) from framework handlers in `backend/tests/integration/logging/test_dual_output_files.py`

**Checkpoint**: US3 fully functional and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation synchronization, and roadmap state consistency

- [X] T034 [P] Update EN-0200 validation and operational steps in `specs/001-logging-baseline-rotation/quickstart.md`
- [X] T035 [P] Update observability documentation in `README.md` and `backend/README.md`
- [X] T036 [P] Synchronize observability baseline references across feature docs in `docs/spec/features/*.md`
- [X] T037 Run backend quality gates (`ruff`, `mypy`, `pytest`) and record evidence in `specs/001-logging-baseline-rotation/plan.md`
- [X] T038 Run existing contract regression suite to confirm no external surface changes in `backend/tests/contract/auth/test_bootstrap_contract.py`, `backend/tests/contract/auth/test_login_logout_contract.py`, and `backend/tests/contract/auth/test_password_change_contract.py`
- [X] T039 Update EN-0200 status transitions in `docs/spec/roadmap.md` (`planned` -> `in_progress` -> `done`) aligned with implementation progress
- [X] T040 Update `EN-0200` status in `docs/spec/dependency-graph.yaml` aligned with roadmap status

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup): starts immediately
- Phase 2 (Foundational): depends on Phase 1 and blocks all user stories
- Phase 3 (US1): depends on Phase 2
- Phase 4 (US2): depends on Phase 2 and reuses US1 logging emission points
- Phase 5 (US3): depends on Phase 2 and can run after US1/US2 are stable
- Phase 6 (Polish): depends on all selected user stories

### User Story Dependencies

- **US1 (P1)**: no dependency on other stories
- **US2 (P2)**: depends on foundational bootstrap and correlation-aware logging wiring from US1 paths
- **US3 (P3)**: depends on foundational framework profile loading and handler configuration

### Within Each User Story

- Write tests first and confirm failing behavior (TDD)
- Implement minimal code to pass tests
- Refactor while preserving green tests
- Complete story checkpoint before moving to next priority

### Dependency Graph

- Foundation -> US1 -> US2
- Foundation -> US3
- US1 + US2 + US3 -> Polish

## Parallel Opportunities

- Setup: T002 and T003 can run in parallel after T001
- Foundation: T006 and T007 can run in parallel after T004/T005
- US1: T012/T013/T041/T042 in parallel; T014/T015/T016 in parallel
- US2: T019 and T020 in parallel
- US3: T025/T026/T027 in parallel; T028/T029/T030 in parallel
- Polish: T034/T035/T036 in parallel

## Parallel Example: User Story 1

```bash
# Parallel tests for US1
T012 backend/tests/integration/logging/test_required_fields.py
T013 backend/tests/integration/logging/test_sensitive_data_sanitization.py
T041 backend/tests/integration/logging/test_message_language_and_field_naming.py
T042 backend/tests/integration/logging/test_structured_context_fields.py

# Parallel implementation tasks for US1 use cases
T014 backend/src/baku/backend/application/auth/bootstrap_operator.py
T015 backend/src/baku/backend/application/auth/login_operator.py backend/src/baku/backend/application/auth/logout_operator.py
T016 backend/src/baku/backend/application/auth/change_operator_password.py
```

## Parallel Example: User Story 2

```bash
# Parallel tests for US2
T019 backend/tests/integration/logging/test_correlation_propagation.py
T020 backend/tests/integration/logging/test_correlation_generation.py
```

## Parallel Example: User Story 3

```bash
# Parallel tests for US3
T025 backend/tests/integration/logging/test_missing_profile_fallback.py
T026 backend/tests/integration/logging/test_env_profile_selection.py
T027 backend/tests/integration/logging/test_rotation_retention_policy.py

# Parallel env config tasks for US3
T028 backend/logging.dev.ini
T029 backend/logging.test.ini
T030 backend/logging.prod.ini
```

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Setup (Phase 1)
2. Complete Foundational (Phase 2)
3. Complete US1 (Phase 3)
4. Validate US1 independently before widening scope

### Incremental Delivery

1. Deliver US1 (structured logs and sanitization)
2. Deliver US2 (correlation traceability)
3. Deliver US3 (rotation, retention, profile selection, fallback)
4. Execute Polish phase and documentation/state synchronization

### Parallel Team Strategy

1. One stream on foundational logging internals (T004-T011)
2. One stream on US1 behavioral tests and auth use-case instrumentation
3. One stream on root logging profile files and rotation/retention tests once foundation is stable

## Notes

- No new external contract tests are required by versioning policy because EN-0200 does not change HTTP/event contracts.
- Existing contract tests are still executed as regression guards in T038.
- Tasks preserve ADR-0002 boundaries by keeping the app decoupled: framework behavior is controlled in root profile files and app code only bootstraps logging.