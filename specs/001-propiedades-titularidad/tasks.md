# Tasks: F-0003 Propiedades y Titularidad

**Input**: Design documents from `specs/001-propiedades-titularidad/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

**Tests**: Se incluyen pruebas de contrato e integracion por cambio de superficie HTTP y por disciplina TDD obligatoria declarada en spec/constitucion.

**Organization**: Tareas agrupadas por historia de usuario para implementacion y validacion independiente.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Preparar estructura del modulo y baseline documental para iniciar F-0003 en estado `in_progress`.

- [x] T001 Crear estructura de modulo `properties` en `backend/src/baku/backend/domain/properties/`, `backend/src/baku/backend/application/properties/`, `backend/src/baku/backend/infrastructure/persistence/sqlite/properties/` e `backend/src/baku/backend/interfaces/http/api/v1/properties/`
- [x] T002 Actualizar estado de F-0003 a `in_progress` en `docs/roadmap.md`
- [x] T003 Actualizar estado de F-0003 a `in_progress` en `docs/dependency-graph.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Definir cimientos tecnicos que bloquean todas las historias (modelo, persistencia base, wiring y errores tipificados).

**CRITICAL**: Ninguna historia de usuario comienza antes de completar esta fase.

- [x] T004 Definir value objects, enums y errores de dominio compartidos de propiedades/titularidad en `backend/src/baku/backend/domain/properties/value_objects.py`, `backend/src/baku/backend/domain/properties/enums.py` y `backend/src/baku/backend/domain/properties/errors.py`
- [x] T005 Definir puertos/repositorios de dominio para Property y Ownership en `backend/src/baku/backend/domain/properties/repositories.py`
- [x] T006 Definir contratos base de aplicacion (DTOs internos y puertos de casos de uso) en `backend/src/baku/backend/application/properties/contracts.py`
- [x] T007 Crear modelos ORM y mapeadores base de propiedades/titularidad en `backend/src/baku/backend/infrastructure/persistence/sqlite/properties/models.py` y `backend/src/baku/backend/infrastructure/persistence/sqlite/properties/mappers.py`
- [x] T008 Registrar repositorios de infraestructura de propiedades/titularidad en `backend/src/baku/backend/infrastructure/persistence/sqlite/properties/repositories.py`
- [x] T009 Integrar wiring de dependencias de modulo properties en `backend/src/baku/backend/interfaces/http/dependency_wiring.py`
- [x] T010 Definir mapeo de errores tipificados de properties en `backend/src/baku/backend/interfaces/http/api/v1/error_mapping.py`
- [x] T011 Integrar configuracion transversal de paginacion (`page_size`, `max_page_size`) en `backend/src/baku/backend/infrastructure/config/runtime_settings.py` y `backend/src/baku/backend/infrastructure/config/validator.py`
- [x] T012 Crear contrato OpenAPI de F-0003 en `specs/001-propiedades-titularidad/contracts/properties-api-v1.yaml` alineado con `backend/src/baku/backend/interfaces/http/api/v1/properties/`

**Checkpoint**: Base lista para implementar historias en paralelo.

---

## Phase 3: User Story 1 - Registrar propiedad con titularidad inicial (Priority: P1) 🎯 MVP

**Goal**: Permitir alta de propiedad con titularidad inicial valida y auditoria completa.

**Independent Test**: Crear propiedad con titulares validos, verificar 201, metadatos de auditoria y rechazo de payloads invalidos.

### Tests for User Story 1

- [x] T013 [P] [US1] Crear pruebas de contrato de alta de propiedad en `backend/tests/contract/properties/test_create_property_contract.py`
- [x] T014 [P] [US1] Crear pruebas de integracion de alta con titularidad inicial en `backend/tests/integration/properties/test_create_property_flow.py`

### Implementation for User Story 1

- [x] T015 [P] [US1] Implementar entidad Property y reglas de creacion en `backend/src/baku/backend/domain/properties/entities.py`
- [x] T016 [P] [US1] Implementar entidad Ownership y validaciones de porcentaje/unicidad logica en `backend/src/baku/backend/domain/properties/entities.py`
- [x] T017 [US1] Implementar caso de uso `create_property` en `backend/src/baku/backend/application/properties/create_property.py`
- [x] T018 [US1] Implementar endpoint `POST /api/v1/properties` y schema request/response en `backend/src/baku/backend/interfaces/http/api/v1/properties/router.py` y `backend/src/baku/backend/interfaces/http/api/v1/properties/schemas.py`
- [x] T019 [US1] Implementar persistencia transaccional de alta de propiedad y titularidad inicial en `backend/src/baku/backend/infrastructure/persistence/sqlite/properties/repositories.py`
- [x] T020 [US1] Añadir serializacion sin campos `null` para responses de alta en `backend/src/baku/backend/interfaces/http/api/v1/properties/serializers.py`

**Checkpoint**: US1 funcional y demostrable como MVP.

---

## Phase 4: User Story 2 - Consultar propiedades y relaciones de titularidad (Priority: P2)

**Goal**: Consultar detalle/listados de propiedades y relaciones activas con paginacion consistente.

**Independent Test**: Listar propiedades paginadas, obtener detalle, consultar propietarios de una propiedad y propiedades por propietario.

### Tests for User Story 2

- [x] T021 [P] [US2] Crear pruebas de contrato de consultas y paginacion de propiedades en `backend/tests/contract/properties/test_property_queries_contract.py`
- [x] T022 [P] [US2] Crear pruebas de integracion de consultas cruzadas propiedad-propietario en `backend/tests/integration/properties/test_property_query_flows.py`

### Implementation for User Story 2

- [x] T023 [US2] Implementar casos de uso de consulta (`list_properties`, `get_property_detail`, `list_property_owners`, `list_owner_properties`) en `backend/src/baku/backend/application/properties/query_properties.py`
- [x] T024 [US2] Implementar consultas de persistencia con filtros activos y paginacion en `backend/src/baku/backend/infrastructure/persistence/sqlite/properties/repositories.py`
- [x] T025 [US2] Implementar endpoints `GET /api/v1/properties`, `GET /api/v1/properties/{property_id}`, `GET /api/v1/properties/{property_id}/owners`, `GET /api/v1/owners/{owner_id}/properties` en `backend/src/baku/backend/interfaces/http/api/v1/properties/router.py`
- [x] T026 [US2] Aplicar defaults y limites de paginacion desde configuracion centralizada en `backend/src/baku/backend/interfaces/http/api/v1/properties/pagination.py`

**Checkpoint**: US2 funcional de forma independiente sobre datos activos.

---

## Phase 5: User Story 3 - Actualizar propiedad y titularidad actual (Priority: P3)

**Goal**: Editar campos permitidos de propiedad y reemplazar/ajustar titularidades actuales con invariantes.

**Independent Test**: Actualizar propiedad y titularidad, verificando reglas de porcentaje, precision y no edicion de derivados.

### Tests for User Story 3

- [x] T027 [P] [US3] Crear pruebas de contrato de actualizacion de propiedad y ownership en `backend/tests/contract/properties/test_update_property_contract.py`
- [x] T028 [P] [US3] Crear pruebas de integracion de invariantes de actualizacion en `backend/tests/integration/properties/test_update_property_invariants.py`

### Implementation for User Story 3

- [x] T029 [US3] Implementar caso de uso `update_property` en `backend/src/baku/backend/application/properties/update_property.py`
- [x] T030 [US3] Implementar caso de uso `replace_property_ownership` en `backend/src/baku/backend/application/properties/update_ownership.py`
- [x] T031 [US3] Implementar reglas de bloqueo de campos derivados y sumatoria de ownership en `backend/src/baku/backend/domain/properties/policies.py`
- [x] T032 [US3] Implementar endpoints `PATCH /api/v1/properties/{property_id}` y `PUT /api/v1/properties/{property_id}/ownership` en `backend/src/baku/backend/interfaces/http/api/v1/properties/router.py`

**Checkpoint**: US3 funcional y validable sin depender de US4.

---

## Phase 6: User Story 4 - Eliminar propiedad con soft-delete (Priority: P4)

**Goal**: Dar de baja logica una propiedad y aplicar soft-delete en cascada sobre titularidades activas.

**Independent Test**: Eliminar propiedad, verificar exclusion de consultas activas y soft-delete en cascada de titularidades.

### Tests for User Story 4

- [x] T033 [P] [US4] Crear pruebas de contrato de soft-delete de propiedad en `backend/tests/contract/properties/test_delete_property_contract.py`
- [x] T034 [P] [US4] Crear pruebas de integracion de cascada de soft-delete en titularidades en `backend/tests/integration/properties/test_property_soft_delete_cascade.py`

### Implementation for User Story 4

- [x] T035 [US4] Implementar caso de uso `delete_property` con cascada de titularidades en `backend/src/baku/backend/application/properties/delete_property.py`
- [x] T036 [US4] Implementar soft-delete en persistencia para propiedad y ownership asociada en `backend/src/baku/backend/infrastructure/persistence/sqlite/properties/repositories.py`
- [x] T037 [US4] Implementar endpoint `DELETE /api/v1/properties/{property_id}` en `backend/src/baku/backend/interfaces/http/api/v1/properties/router.py`

**Checkpoint**: US4 funcional con trazabilidad auditable.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de calidad, documentacion y sincronizacion de roadmap.

- [x] T038 [P] Actualizar documentacion funcional de la feature en `docs/spec/features/F-0003-propiedades-y-titularidad.md` para alinear dependencias declaradas con DAG
- [x] T039 [P] Actualizar documentacion de uso en `backend/README.md`
- [x] T040 [P] Actualizar resumen de capacidades en `README.md`
- [x] T041 Ejecutar validacion completa de quickstart F-0003 en `specs/001-propiedades-titularidad/quickstart.md`
- [x] T042 Ejecutar quality gates (`ruff`, `mypy`, `pytest`) en `backend/`
- [x] T043 Actualizar estado de F-0003 a `done` en `docs/roadmap.md`
- [x] T044 Actualizar estado de F-0003 a `done` en `docs/dependency-graph.yaml`

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup): inicia inmediatamente.
- Phase 2 (Foundational): depende de Phase 1 y bloquea todas las historias.
- Phases 3-6 (US1-US4): dependen de Phase 2.
- Phase 7 (Polish): depende de completar las historias objetivo.

### User Story Dependencies

- US1 (P1): inicia tras Foundational y habilita el MVP.
- US2 (P2): inicia tras Foundational; puede ejecutarse en paralelo con US3 si hay capacidad.
- US3 (P3): inicia tras Foundational; depende funcionalmente de entidades y consultas ya definidas.
- US4 (P4): inicia tras Foundational; se apoya en modelo de persistencia de US1-US3.

### Within Each User Story

- Tests primero y en rojo antes de implementacion.
- Casos de uso antes de endpoints.
- Persistencia y mapeo de errores antes de cerrar historia.

### Dependency Graph Issue

- El DAG oficial exige `F-0003 -> F-0002`, pero `docs/spec/features/F-0003-propiedades-y-titularidad.md` aun indica "(ninguna explicita)". Las tareas siguen el DAG como fuente de verdad y agregan sincronizacion documental (T038).

---

## Parallel Opportunities

- Tareas marcadas con `[P]` pueden ejecutarse en paralelo.
- Tras Phase 2, pruebas y desarrollo de US2/US3 pueden correr en paralelo por equipos distintos.

## Parallel Example: User Story 1

```bash
Task: "T013 [US1] Contract tests de alta de propiedad"
Task: "T014 [US1] Integration tests de alta con titularidad"
Task: "T015 [US1] Entidad Property"
Task: "T016 [US1] Entidad Ownership"
```

## Implementation Strategy

### MVP First (US1)

1. Completar Setup y Foundational.
2. Completar US1.
3. Validar quickstart parcial para alta/consulta basica.

### Incremental Delivery

1. US1 (alta) -> demo.
2. US2 (consultas) -> demo.
3. US3 (actualizacion) -> demo.
4. US4 (baja logica) -> demo.
5. Polish y sincronizacion documental final.

### Parallel Team Strategy

1. Equipo completo en Phase 1 y 2.
2. Luego dividir por historias:
   - Dev A: US2
   - Dev B: US3
   - Dev C: US4
3. Consolidar con pruebas de contrato/integracion y cierre documental.
