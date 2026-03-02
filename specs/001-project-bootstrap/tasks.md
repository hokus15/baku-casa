# Tasks: EN-0100 Project Bootstrap

**Input**: Design documents from `/specs/001-project-bootstrap/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Este enabler requiere pruebas mínimas explícitas (smoke tests por root) y validación CI en PR (`lint + tipado + smoke tests`).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicializar estructura base de trabajo para el enabler

- [X] T001 Crear estructura base de documentación del enabler en specs/001-project-bootstrap/
- [X] T002 [P] Verificar existencia de docs base en docs/spec/ y docs/adr/
- [X] T003 [P] Asegurar README raíz con validaciones básicas en README.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Base técnica obligatoria previa a cualquier historia

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Crear root backend mínimo con pyproject y carpetas base en backend/pyproject.toml
- [X] T005 Crear root bot mínimo con pyproject y carpetas base en bot/pyproject.toml
- [X] T006 [P] Añadir marcador de código base en backend/src/
- [X] T007 [P] Añadir marcador de código base en bot/src/
- [X] T008 Configurar estructura mínima de tests en backend/tests/
- [X] T009 Configurar estructura mínima de tests en bot/tests/
- [X] T010 Definir workflow CI para PR con jobs por root en .github/workflows/bootstrap-pr.yml

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Base mínima reproducible del repositorio (Priority: P1) 🎯 MVP

**Goal**: Tener bootstrap multi-root con artefactos mínimos y documentación base sin lógica de dominio

**Independent Test**: Se valida comprobando existencia de roots `backend` y `bot` con estructura mínima y documentación base sin endpoints/lógica de dominio

### Implementation for User Story 1

- [X] T011 [US1] Verificar estructura mínima del root backend (`src/`, `tests/`) en backend/
- [X] T012 [US1] Verificar estructura mínima del root bot (`src/`, `tests/`) en bot/
- [X] T013 [P] [US1] Añadir README de root backend en backend/README.md
- [X] T014 [P] [US1] Añadir README de root bot en bot/README.md
- [X] T015 [US1] Actualizar README raíz con descripción del bootstrap y validaciones básicas en README.md
- [X] T016 [US1] Verificar que no se introducen endpoints ni lógica de dominio en backend/src/ y bot/src/

**Checkpoint**: US1 completa y verificable de forma independiente

---

## Phase 4: User Story 2 - Validación automática mínima por root (Priority: P2)

**Goal**: Ejecutar en PR `lint + tipado + smoke tests` por root con resultado visible

**Independent Test**: Abrir PR de prueba y confirmar ejecución de lint, tipado y smoke tests en backend y bot

### Tests for User Story 2

- [X] T017 [P] [US2] Crear smoke test mínimo de backend en backend/tests/
- [X] T018 [P] [US2] Crear smoke test mínimo de bot en bot/tests/

### Implementation for User Story 2

- [X] T019 [US2] Configurar job CI de backend (lint, tipado, smoke) en .github/workflows/bootstrap-pr.yml
- [X] T020 [US2] Configurar job CI de bot (lint, tipado, smoke) en .github/workflows/bootstrap-pr.yml
- [X] T021 [US2] Asegurar fallo explícito de CI cuando falte un check requerido en .github/workflows/bootstrap-pr.yml
- [X] T031 [US2] Añadir validación de ejecución CI sin servicios externos obligatorios y con límites de tiempo en .github/workflows/bootstrap-pr.yml
- [X] T022 [US2] Documentar ejecución local mínima de checks por root en README.md

**Checkpoint**: US2 completa y verificable de forma independiente

---

## Phase 5: User Story 3 - Aislamiento del alcance del enabler (Priority: P3)

**Goal**: Garantizar que EN-0100 permanece estrictamente habilitador y sin alcance funcional de dominio

**Independent Test**: Revisar código y CI para confirmar ausencia de endpoints, persistencia funcional y eventos

### Implementation for User Story 3

- [X] T023 [US3] Añadir regla de control de alcance en documentación del enabler en specs/001-project-bootstrap/quickstart.md
- [X] T024 [US3] Añadir verificación CI para impedir endpoints reales en bootstrap en .github/workflows/bootstrap-pr.yml
- [X] T025 [US3] Añadir verificación CI para impedir migraciones/eventos en bootstrap en .github/workflows/bootstrap-pr.yml
- [X] T030 [US3] Añadir verificación CI para bloquear imports runtime cruzados entre backend y bot en .github/workflows/bootstrap-pr.yml
- [X] T026 [US3] Confirmar ausencia de cambios de contrato y versionado funcional en specs/001-project-bootstrap/contracts/no-contract-changes.md

**Checkpoint**: US3 completa y verificable de forma independiente

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de consistencia y preparación para siguiente fase

- [X] T027 [P] Consolidar quickstart final y gates de salida en specs/001-project-bootstrap/quickstart.md
- [X] T028 [P] Revisar trazabilidad spec-plan-research-data model-contracts en specs/001-project-bootstrap/
- [X] T029 Ejecutar validación final de artefactos del enabler en specs/001-project-bootstrap/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependency on other stories
- **User Story 2 (P2)**: Depends on US1 structure (`backend/`, `bot/` y tests base)
- **User Story 3 (P3)**: Depends on US1 + US2 para validar alcance en código y CI

### Within Each User Story

- Artefactos base antes que validaciones
- Smoke tests antes de endurecer CI
- Reglas de alcance al final para bloquear deriva

### Dependency Graph

- US1 → US2 → US3

---

## Parallel Opportunities

- **Setup**: T002 y T003 en paralelo
- **Foundational**: T006 y T007 en paralelo
- **US1**: T013 y T014 en paralelo
- **US2**: T017 y T018 en paralelo
- **Polish**: T027 y T028 en paralelo

## Parallel Example: User Story 2

```bash
# Smoke tests por root en paralelo
Task: "Crear smoke test mínimo de backend en backend/tests/"
Task: "Crear smoke test mínimo de bot en bot/tests/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup
2. Complete Foundational
3. Complete User Story 1
4. Validate US1 independently

### Incremental Delivery

1. US1: Estructura mínima reproducible
2. US2: CI mínima por root (`lint + tipado + smoke`)
3. US3: Endurecimiento de alcance del enabler
4. Polish y validación final

### Parallel Team Strategy

1. Developer A: Root backend + smoke test backend
2. Developer B: Root bot + smoke test bot
3. Developer C: Workflow CI + validaciones de alcance

---

## Notes

- Todas las tareas siguen formato checklist ejecutable
- No se incluyen migraciones ni contratos funcionales nuevos en EN-0100
- Si durante implementación surge necesidad de alterar ADR, registrar como ADR Gap antes de continuar
