# Tasks: F-0002 Propietarios (Sujetos fiscales)

**Input**: Design documents from `specs/001-propietarios-sujetos-fiscales/`  
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`

**Tests**: Contract tests are MANDATORY because F-0002 introduces a new HTTP contract surface (`/api/v1/owners`). Integration and domain/application tests are required by Constitution and plan.

**Organization**: Tasks are grouped by user story and ordered to respect DAG and architectural constraints.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no direct dependency)
- **[Story]**: US1, US2, US3, US4, US5
- Include exact file paths in descriptions

---

## Dependency Graph Check

- Declared dependency for F-0002 (`F-0001`) is satisfied.
- Applicable completed enablers assumed as baseline: `EN-0100`, `EN-0202`, `EN-0200`, `EN-0201`, `EN-0300`.
- No task depends on future roadmap items (`F-0003+`, `EN-0207`, `EN-0301`, etc.).

**Dependency Graph Issue**: None.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Crear estructura base del modulo de owners sin romper arquitectura hexagonal.

- [X] T001 Crear paquete de dominio de owners en `backend/src/baku/backend/domain/owners/__init__.py`
- [X] T002 [P] Crear paquete de aplicación de owners en `backend/src/baku/backend/application/owners/__init__.py`
- [X] T003 [P] Crear paquete de infraestructura de persistencia de owners en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/__init__.py`
- [X] T004 [P] Crear paquete de interfaz HTTP v1 de owners en `backend/src/baku/backend/interfaces/http/api/v1/owners/__init__.py`
- [X] T005 [P] Crear estructura de tests de contrato de owners en `backend/tests/contract/owners/__init__.py`
- [X] T006 [P] Crear estructura de tests de integración de owners en `backend/tests/integration/owners/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Construir base técnica reusable para todas las historias de usuario de la feature.

**⚠️ CRITICAL**: Ninguna historia puede comenzar antes de completar esta fase.

- [X] T007 Definir errores tipificados de owners en `backend/src/baku/backend/domain/owners/errors.py`
- [X] T008 [P] Definir enumeración `EntityType` en `backend/src/baku/backend/domain/owners/value_objects.py`
- [X] T009 [P] Definir entidad de dominio `Owner` y reglas de invariantes en `backend/src/baku/backend/domain/owners/entities.py`
- [X] T010 Definir normalizador de `tax_id` en `backend/src/baku/backend/domain/owners/tax_id_normalizer.py`
- [X] T011 Definir puertos/repositorios de owners en `backend/src/baku/backend/domain/owners/repositories.py`
- [X] T012 [P] Definir modelos ORM de owners (tabla `owners`, columnas en ingles) en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/models.py`
- [X] T013 Implementar mapeadores ORM <-> dominio de owners en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/mappers.py`
- [X] T014 Implementar repositorio SQLite de owners en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/repositories.py`
- [X] T015 Preparar migración versionada para esquema de owners (sin SQL inline en tareas) en `backend/migrations/versions/`
- [X] T016 Definir DTOs HTTP de owners con nombres de campos en ingles en `backend/src/baku/backend/interfaces/http/api/v1/owners/schemas.py`
- [X] T017 Definir mapeo de errores owners -> HTTP status en `backend/src/baku/backend/interfaces/http/error_mapper.py`
- [X] T018 Registrar wiring base de dependencias (proveedores de repositorio e infraestructura comun) en `backend/src/baku/backend/interfaces/http/dependency_wiring.py`

**Checkpoint**: Foundation ready.

---

## Phase 3: User Story 1 - Create owner (Priority: P1) 🎯 MVP

**Goal**: Crear propietario con validaciones, auditoría y unicidad por `tax_id` normalizado.

**Independent Test**: `POST /api/v1/owners` crea owner válido; conflicto por `tax_id` duplicado; errores tipificados con `correlation_id`.

### Tests for US1 (write first)

- [X] T019 [P] [US1] Contract test de `POST /api/v1/owners` (201/400/401/409) en `backend/tests/contract/owners/test_create_owner_contract.py`
- [X] T020 [P] [US1] Integration test de creación con default `fiscal_address_country=ES` en `backend/tests/integration/owners/test_create_owner_flow.py`
- [X] T021 [P] [US1] Domain test de normalización y unicidad de `tax_id` en `backend/tests/integration/owners/test_tax_id_normalization.py`

### Implementation for US1

- [X] T022 [US1] Implementar caso de uso `CreateOwner` en `backend/src/baku/backend/application/owners/create_owner.py`
- [X] T023 [US1] Implementar endpoint `POST /api/v1/owners` en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`
- [X] T024 [US1] Asegurar captura de `created_by`/`updated_by` desde identidad autenticada en `backend/src/baku/backend/application/owners/create_owner.py`
- [X] T025 [US1] Agregar logging estructurado sin PII para create en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`

**Checkpoint**: US1 funcional y testeable independientemente.

---

## Phase 4: User Story 2 - Owner detail retrieval (Priority: P2)

**Goal**: Consultar detalle por `owner_id` con soporte `include_deleted` (default `false`).

**Independent Test**: `GET /api/v1/owners/{owner_id}` retorna owner activo; retorna 404 cuando no existe o está borrado y `include_deleted=false`.

### Tests for US2 (write first)

- [X] T026 [P] [US2] Contract test de `GET /api/v1/owners/{owner_id}` en `backend/tests/contract/owners/test_get_owner_detail_contract.py`
- [X] T027 [P] [US2] Integration test de `include_deleted` en detalle en `backend/tests/integration/owners/test_get_owner_detail_flow.py`
- [ ] T059 [P] [US2] Observability test: logs de detail incluyen `correlation_id` y excluyen PII en `backend/tests/integration/owners/test_get_owner_detail_observability.py`

### Implementation for US2

- [X] T028 [US2] Implementar caso de uso `GetOwnerById` en `backend/src/baku/backend/application/owners/get_owner_by_id.py`
- [X] T029 [US2] Implementar endpoint `GET /api/v1/owners/{owner_id}` en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`
- [X] T030 [US2] Implementar filtro de soft-delete en repositorio para detalle en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/repositories.py`
- [X] T060 [US2] Agregar logging estructurado sin PII para detail en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`

**Checkpoint**: US2 funcional y testeable independientemente.

---

## Phase 5: User Story 3 - List and search owners (Priority: P3)

**Goal**: Listar y buscar owners con paginación, filtros (`tax_id`, `legal_name`) y `include_deleted`.

**Independent Test**: `GET /api/v1/owners` retorna estructura paginada consistente y filtra correctamente.

### Tests for US3 (write first)

- [X] T031 [P] [US3] Contract test de `GET /api/v1/owners` (200/400/401) en `backend/tests/contract/owners/test_list_owners_contract.py`
- [X] T032 [P] [US3] Integration test de paginación y `page_size` cap en `backend/tests/integration/owners/test_list_owners_pagination.py`
- [X] T033 [P] [US3] Integration test de filtros por `tax_id` y `legal_name` en `backend/tests/integration/owners/test_list_owners_filters.py`
- [ ] T061 [P] [US3] Observability test: logs de list incluyen `correlation_id` y excluyen PII en `backend/tests/integration/owners/test_list_owners_observability.py`

### Implementation for US3

- [X] T034 [US3] Implementar caso de uso `ListOwners` en `backend/src/baku/backend/application/owners/list_owners.py`
- [X] T035 [US3] Implementar endpoint `GET /api/v1/owners` en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`
- [X] T036 [US3] Implementar consulta paginada/filtros en repositorio SQLite en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/repositories.py`
- [X] T062 [US3] Agregar logging estructurado sin PII para list en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`

**Checkpoint**: US3 funcional y testeable independientemente.

---

## Phase 6: User Story 4 - Update owner (Priority: P4)

**Goal**: Editar owner activo manteniendo `owner_id` inmutable y conflicto por `tax_id`.

**Independent Test**: `PATCH /api/v1/owners/{owner_id}` actualiza campos permitidos, rechaza conflictos y no permite alterar `owner_id`.

### Tests for US4 (write first)

- [X] T037 [P] [US4] Contract test de `PATCH /api/v1/owners/{owner_id}` en `backend/tests/contract/owners/test_update_owner_contract.py`
- [X] T038 [P] [US4] Integration test de conflicto por `tax_id` en `backend/tests/integration/owners/test_update_owner_conflict.py`
- [ ] T039 [P] [US4] Integration test de inmutabilidad de `owner_id` en `backend/tests/integration/owners/test_update_owner_immutable_id.py`
- [ ] T063 [P] [US4] Observability test: logs de update incluyen `correlation_id` y excluyen PII en `backend/tests/integration/owners/test_update_owner_observability.py`

### Implementation for US4

- [X] T040 [US4] Implementar caso de uso `UpdateOwner` en `backend/src/baku/backend/application/owners/update_owner.py`
- [X] T041 [US4] Implementar endpoint `PATCH /api/v1/owners/{owner_id}` en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`
- [X] T042 [US4] Actualizar reglas de repositorio para write en activos y refresh de `updated_at`/`updated_by` en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/repositories.py`
- [X] T064 [US4] Agregar logging estructurado sin PII para update en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`

**Checkpoint**: US4 funcional y testeable independientemente.

---

## Phase 7: User Story 5 - Soft delete owner (Priority: P5)

**Goal**: Soft delete auditable (`deleted_at`, `deleted_by`) sin borrado físico.

**Independent Test**: `DELETE /api/v1/owners/{owner_id}` marca borrado lógico; owner no aparece por defecto y reaparece con `include_deleted=true`.

### Tests for US5 (write first)

- [X] T043 [P] [US5] Contract test de `DELETE /api/v1/owners/{owner_id}` en `backend/tests/contract/owners/test_delete_owner_contract.py`
- [X] T044 [P] [US5] Integration test de comportamiento post-delete en list/detail en `backend/tests/integration/owners/test_soft_delete_owner_flow.py`
- [X] T045 [P] [US5] Integration test de delete repetido -> 404 en `backend/tests/integration/owners/test_soft_delete_owner_idempotency.py`
- [ ] T065 [P] [US5] Observability test: logs de delete incluyen `correlation_id` y excluyen PII en `backend/tests/integration/owners/test_soft_delete_owner_observability.py`

### Implementation for US5

- [X] T046 [US5] Implementar caso de uso `SoftDeleteOwner` en `backend/src/baku/backend/application/owners/soft_delete_owner.py`
- [X] T047 [US5] Implementar endpoint `DELETE /api/v1/owners/{owner_id}` en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`
- [X] T048 [US5] Persistir soft delete auditable en repositorio (`deleted_at`, `deleted_by`) en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/repositories.py`
- [X] T066 [US5] Agregar logging estructurado sin PII para delete en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`

**Checkpoint**: US5 funcional y testeable independientemente.

---

## Phase 8: Integration, Wiring, and Documentation Sync

**Purpose**: Cierre transversal de contrato, wiring, observabilidad, CI y documentación.

- [X] T049 Registrar router de owners en app factory/composition root en `backend/src/baku/backend/interfaces/http/app_factory.py`
- [X] T050 Verificar autenticación obligatoria en todos los endpoints owners en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`
- [X] T051 [P] Alinear contrato OpenAPI con implementación real en `specs/001-propietarios-sujetos-fiscales/contracts/owners-api-v1.yaml`
- [X] T052 [P] Alinear catálogo de errores owners con mapeo real en `specs/001-propietarios-sujetos-fiscales/contracts/error-model.md`
- [X] T053 [P] Ejecutar quickstart completo y registrar resultados en `specs/001-propietarios-sujetos-fiscales/quickstart.md`
- [X] T054 [P] Actualizar documentación de endpoints owners en `backend/README.md`
- [X] T055 Confirmar que `bot/README.md` no requiere cambios para F-0002; documentar verificación en `specs/001-propietarios-sujetos-fiscales/plan.md`
- [X] T056 Cambiar estado F-0002 a `in_progress` en `docs/spec/roadmap.md` y `docs/spec/dependency-graph.yaml` al iniciar implementación
- [X] T057 Cambiar estado F-0002 a `done` en `docs/spec/roadmap.md` y `docs/spec/dependency-graph.yaml` al cerrar implementación
- [X] T058 Ejecutar gates de calidad (`ruff`, `mypy`, `pytest`) y registrar evidencia en `backend/README.md`
- [X] T067 Completar wiring final de casos de uso de owners en `backend/src/baku/backend/interfaces/http/dependency_wiring.py`
- [ ] T068 [P] Definir y documentar prueba automatizada de ruta backup -> migrate -> restore -> integrity para owners en `backend/tests/integration/owners/test_owner_migration_restore_path.py`
- [X] T069 [P] Ejecutar y evidenciar verificación de backup/restore asociada a la migración de owners en `specs/001-propietarios-sujetos-fiscales/quickstart.md`

---

## Phase 9: Model Evolution - New Owner Fields (entity/contact)

**Purpose**: Adaptar F-0002 al nuevo modelo de campos (`entity_type`, identidad extendida y contacto extendido) sin romper arquitectura ni contrato versionado.

- [X] T070 [P] Evolucionar entidad de dominio Owner para usar `entity_type` y agregar `first_name`, `last_name`, `stamp_image`, `land_line`, `land_line_country_code`, `mobile`, `mobile_country_code` en `backend/src/baku/backend/domain/owners/entities.py`
- [X] T071 [P] Ajustar enumeración de tipos de entidad a `{PERSONA_FISICA, PERSONA_JURIDICA, ESPJ}` en `backend/src/baku/backend/domain/owners/value_objects.py`
- [X] T072 Actualizar contratos de repositorio y mapeadores dominio/ORM para los nuevos campos en `backend/src/baku/backend/domain/owners/repositories.py` y `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/mappers.py`
- [X] T073 Implementar migración de esquema para consolidar `entity_type` y el nuevo set de campos de owners en `backend/migrations/versions/`
- [X] T074 Actualizar modelo ORM de owners con nuevas columnas y defaults de `*_country_code` en `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/models.py`
- [X] T075 Actualizar DTOs y validaciones HTTP (`OwnerCreateRequest`, `OwnerUpdateRequest`, `OwnerResponse`) con `entity_type` y contacto extendido en `backend/src/baku/backend/interfaces/http/api/v1/owners/schemas.py`
- [X] T076 Actualizar casos de uso Create/Update para persistir nuevos campos y tratar vacíos de contacto como ausentes en `backend/src/baku/backend/application/owners/create_owner.py` y `backend/src/baku/backend/application/owners/update_owner.py`
- [X] T077 Actualizar router de owners para mapear payloads nuevos y mantener omisión de campos `null` en `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py`
- [X] T078 [P] Actualizar contract tests de owners para `entity_type` y campos nuevos en `backend/tests/contract/owners/test_create_owner_contract.py` y `backend/tests/contract/owners/test_update_owner_contract.py`
- [X] T079 [P] Actualizar integration tests de create/detail/list/update con nuevos campos y country codes en `backend/tests/integration/owners/test_create_owner_flow.py` y `backend/tests/integration/owners/test_get_owner_detail_flow.py`
- [X] T080 [P] Alinear OpenAPI de owners con `entity_type` y payloads extendidos en `specs/001-propietarios-sujetos-fiscales/contracts/owners-api-v1.yaml`
- [X] T081 [P] Alinear `data-model.md` con `EntityType` y nuevos campos de identidad/contacto en `specs/001-propietarios-sujetos-fiscales/data-model.md`
- [X] T082 [P] Actualizar quickstart y README backend para ejemplos de request/response con nuevos campos en `specs/001-propietarios-sujetos-fiscales/quickstart.md` y `backend/README.md`

**Checkpoint**: Modelo de campos de owners actualizado y validado por tests sin regressions.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: sin dependencias.
- **Phase 2 (Foundational)**: depende de Phase 1 y bloquea todas las US.
- **Phase 3-7 (User Stories)**: dependen de Foundational; se recomienda ejecutar en prioridad P1 -> P5.
- **Phase 8 (Integration/Docs)**: depende de completar historias deseadas.
- **Phase 9 (Model Evolution)**: depende de Phase 8 para baseline estable; puede ejecutarse como mini-proyecto incremental centrado en renombre/extensión de campos.

### User Story Dependencies

- **US1 (P1)**: inicia tras Foundational.
- **US2 (P2)**: depende de US1 (requiere owner existente).
- **US3 (P3)**: depende de US1 (requiere data creada).
- **US4 (P4)**: depende de US1 y se valida mejor tras US2.
- **US5 (P5)**: depende de US1 y se valida mejor junto a US2/US3 por `include_deleted`.

### Within Each User Story

- Tests first (deben fallar antes de implementar).
- Dominio/puertos antes de casos de uso.
- Casos de uso antes de endpoints.
- Endpoint y mapper de errores antes de cierre de historia.

---

## Parallel Opportunities

- Setup: T002-T006 paralelizables.
- Foundational: T008, T009, T012, T016 paralelizables.
- US tests: tareas `[P]` de cada historia pueden ejecutarse en paralelo.
- Docs sync: T051-T055 y T069 pueden correrse en paralelo una vez implementada la feature.
- Model evolution: T070-T071-T074-T075 y T078-T082 tienen amplias oportunidades de paralelización controlada por conflictos de archivo.

---

## Notes

- Las tareas respetan ADRs activos: hexagonal (ADR-0002), persistencia/migraciones (ADR-0003), HTTP versionado (ADR-0004/0006), errores y observabilidad (ADR-0009), UTC (ADR-0012).
- No se introducen decisiones arquitectónicas nuevas.
- No se incluyen migraciones concretas ni código en este documento.
