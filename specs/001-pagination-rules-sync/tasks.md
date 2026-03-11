# Tasks: Alineacion de reglas de paginacion en F-0001/F-0002/F-0003

**Input**: Design documents from `specs/001-pagination-rules-sync/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Contract tests are required when collection contract behavior changes. Integration tests are required to validate precedence resolution and bounded collection behavior.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Preparar el alcance de sincronizacion documental y de validacion para las tres features implementadas.

- [X] T001 Consolidar matriz de superficies de coleccion/listado/busqueda en `specs/001-pagination-rules-sync/research.md`
- [X] T002 [P] Definir checklist de verificacion de precedencia EN-0202 en `specs/001-pagination-rules-sync/quickstart.md`
- [X] T003 [P] Registrar contrato de gobernanza de paginacion en `specs/001-pagination-rules-sync/contracts/pagination-governance.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establecer una base comun antes de tocar historias de usuario.

**CRITICAL**: No iniciar tareas de historias hasta completar esta fase.

- [X] T004 Establecer regla transversal de paginacion obligatoria en `specs/001-pagination-rules-sync/data-model.md`
- [X] T005 [P] Definir clasificacion de impacto contractual (non-breaking esperado) en `specs/001-pagination-rules-sync/plan.md`
- [X] T006 [P] Definir estrategia TDD y quality gates impactados en `specs/001-pagination-rules-sync/plan.md`
- [X] T007 Confirmar consistencia DAG y baseline de EN-0202 en `specs/001-pagination-rules-sync/plan.md`

**Checkpoint**: Fundacion lista para implementar historias.

---

## Phase 3: User Story 1 - Consistencia transversal de listados (Priority: P1) 🎯 MVP

**Goal**: Asegurar que las especificaciones de F-0001/F-0002/F-0003 declaren paginacion obligatoria para listados/busquedas aplicables.

**Independent Test**: Validar por lectura de spec y pruebas de contrato/integracion que no existan colecciones no acotadas.

### Tests for User Story 1

- [X] T008 [P] [US1] Crear prueba de contrato para colecciones paginadas en `backend/tests/contract/test_pagination_mandatory_collections.py`
- [X] T009 [P] [US1] Crear prueba de integracion para respuestas acotadas en `backend/tests/integration/test_collection_responses_are_bounded.py`

### Implementation for User Story 1

- [X] T010 [US1] Alinear regla de paginacion obligatoria para colecciones potenciales en `docs/spec/features/F-0001-acceso-y-autenticacion-operador.md`
- [X] T011 [US1] Alinear regla de paginacion obligatoria para listados y busquedas en `docs/spec/features/F-0002-propietarios-sujetos-fiscales.md`
- [X] T012 [US1] Verificar y ajustar consistencia de paginacion obligatoria en `docs/spec/features/F-0003-propiedades-y-titularidad.md`
- [X] T013 [US1] Actualizar criterios de aceptacion sincronizados en `specs/001-pagination-rules-sync/spec.md`

**Checkpoint**: US1 implementada y validable de forma independiente.

---

## Phase 4: User Story 2 - Gobernanza de defaults y limites (Priority: P2)

**Goal**: Garantizar que defaults y maximos se resuelven transversalmente via EN-0202 con precedencia global.

**Independent Test**: Validar que la documentacion y pruebas reflejen `environment variables > config file > defaults`.

### Tests for User Story 2

- [X] T014 [P] [US2] Crear prueba de contrato de precedencia de paginacion en `backend/tests/contract/test_pagination_precedence_contract.py`
- [X] T015 [P] [US2] Crear prueba de integracion de precedencia EN-0202 en `backend/tests/integration/test_pagination_precedence_en0202.py`

### Implementation for User Story 2

- [X] T016 [US2] Alinear texto de precedencia global en `docs/spec/features/F-0001-acceso-y-autenticacion-operador.md`
- [X] T017 [US2] Alinear texto de precedencia global en `docs/spec/features/F-0002-propietarios-sujetos-fiscales.md`
- [X] T018 [US2] Alinear texto de precedencia global en `docs/spec/features/F-0003-propiedades-y-titularidad.md`
- [X] T019 [US2] Actualizar contrato de gobernanza con precedencia fija en `specs/001-pagination-rules-sync/contracts/pagination-governance.md`

**Checkpoint**: US2 implementada y validable de forma independiente.

---

## Phase 5: User Story 3 - Eliminacion de hardcodes en comportamiento esperado (Priority: P3)

**Goal**: Eliminar ambiguedad documental que permita defaults o maximos hardcoded fuera de la fuente central.

**Independent Test**: Verificar en specs y contrato que quede explicitamente prohibido hardcode fuera de EN-0202.

### Tests for User Story 3

- [X] T020 [P] [US3] Crear prueba de regresion para detectar defaults hardcoded en colecciones en `backend/tests/contract/test_no_hardcoded_pagination_defaults.py`
- [X] T021 [P] [US3] Crear prueba de integracion para enforcement de maximos configurados en `backend/tests/integration/test_pagination_limits_from_configuration.py`

### Implementation for User Story 3

- [X] T022 [US3] Incorporar prohibicion explicita de hardcodes en `docs/spec/features/F-0001-acceso-y-autenticacion-operador.md`
- [X] T023 [US3] Incorporar prohibicion explicita de hardcodes en `docs/spec/features/F-0002-propietarios-sujetos-fiscales.md`
- [X] T024 [US3] Incorporar prohibicion explicita de hardcodes en `docs/spec/features/F-0003-propiedades-y-titularidad.md`
- [X] T025 [US3] Sincronizar criterio de exito documental sin hardcodes en `specs/001-pagination-rules-sync/spec.md`

**Checkpoint**: US3 implementada y validable de forma independiente.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de coherencia y validacion integral.

- [X] T026 [P] Ejecutar validacion de quickstart en `specs/001-pagination-rules-sync/quickstart.md`
- [X] T027 [P] Verificar que no se requieren cambios de estado en `docs/roadmap.md` ni `docs/dependency-graph.yaml`
- [X] T028 Consolidar trazabilidad final de dependencias y ADR en `specs/001-pagination-rules-sync/plan.md`
- [X] T029 Actualizar checklist de calidad de especificacion en `specs/001-pagination-rules-sync/checklists/requirements.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): inicio inmediato.
- Foundational (Phase 2): depende de Setup y bloquea historias.
- User Stories (Phase 3-5): dependen de Foundational.
- Polish (Phase 6): depende de completar historias seleccionadas.

### User Story Dependencies

- US1 (P1): inicia tras Foundational; define el MVP de consistencia de paginacion.
- US2 (P2): inicia tras Foundational; puede ejecutarse en paralelo con US1 si hay capacidad.
- US3 (P3): inicia tras Foundational; depende conceptualmente de la regla base establecida por US1/US2 para validacion final.

### Within Each User Story

- Escribir primero pruebas y hacerlas fallar.
- Implementar alineacion documental/contractual.
- Ejecutar pruebas y cerrar criterios de historia.

---

## Parallel Opportunities

- T002, T003 pueden ejecutarse en paralelo.
- T005, T006, T007 pueden ejecutarse en paralelo.
- En cada historia, tareas de test marcadas [P] pueden ejecutarse en paralelo.
- T010/T011/T012 y T016/T017/T018 y T022/T023/T024 pueden repartirse en paralelo por archivo.

---

## Parallel Example: User Story 2

- Task: "T014 [US2] Crear prueba de contrato de precedencia de paginacion en backend/tests/contract/test_pagination_precedence_contract.py"
- Task: "T015 [US2] Crear prueba de integracion de precedencia EN-0202 en backend/tests/integration/test_pagination_precedence_en0202.py"
- Task: "T016 [US2] Alinear texto de precedencia global en docs/spec/features/F-0001-acceso-y-autenticacion-operador.md"
- Task: "T017 [US2] Alinear texto de precedencia global en docs/spec/features/F-0002-propietarios-sujetos-fiscales.md"
- Task: "T018 [US2] Alinear texto de precedencia global en docs/spec/features/F-0003-propiedades-y-titularidad.md"

---

## Implementation Strategy

### MVP First (US1)

1. Completar Phase 1 y Phase 2.
2. Completar Phase 3 (US1).
3. Validar criterios independientes de US1.

### Incremental Delivery

1. Entregar US1 (consistencia de paginacion obligatoria).
2. Entregar US2 (precedencia y gobernanza de defaults/maximos).
3. Entregar US3 (prohibicion de hardcodes y cierre de regresiones).
4. Cerrar con Phase 6.

### Parallel Team Strategy

1. Un responsable por cada spec de feature (F-0001/F-0002/F-0003).
2. Un responsable de pruebas contract/integration.
3. Integracion final por responsable de plan/checklist.

---

## Notes

- Todos los tasks siguen formato estricto: `- [ ] T### [P?] [US?] descripcion con ruta`.
- No se introducen migraciones ni decisiones tecnologicas nuevas.
- El alcance es sincronizacion de especificacion y validacion de comportamiento de colecciones.
