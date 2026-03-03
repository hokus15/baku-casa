# Tasks: F-0001 Acceso y Autenticación (Operador)

**Input**: Design documents from `/specs/001-acceso-autenticacion-operador/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Se requieren pruebas de contrato e integración para todos los flujos de autenticación porque F-0001 introduce nueva superficie HTTP versionada y modelo de error tipificado (ADR-0006, ADR-0008).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Crear estructura base de paquetes hexagonales para la feature de autenticación en `backend`

- [X] T001 Crear paquete de dominio de autenticación en backend/src/baku/backend/domain/auth/__init__.py
- [X] T002 [P] Crear paquete de aplicación de autenticación en backend/src/baku/backend/application/auth/__init__.py
- [X] T003 [P] Crear paquete de interfaz HTTP v1 para autenticación en backend/src/baku/backend/interfaces/http/api/v1/__init__.py
- [X] T004a [P] Crear estructura de tests de contrato de autenticación en backend/tests/contract/auth/__init__.py
- [X] T004b [P] Crear estructura de tests de integración de autenticación en backend/tests/integration/auth/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infraestructura transversal obligatoria que todas las historias de usuario necesitan

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Definir configuración de políticas de autenticación (TTL, umbral de intentos, duración de bloqueo) en backend/src/baku/backend/infrastructure/config/auth_settings.py
- [X] T006 [P] Definir errores tipificados de autenticación con códigos estables en inglés en backend/src/baku/backend/domain/auth/errors.py
- [X] T007 [P] Definir entidades de dominio Operator, RevokedToken y LoginThrottleState en backend/src/baku/backend/domain/auth/entities.py
- [X] T008 Definir puertos de repositorio de autenticación (interfaces) en backend/src/baku/backend/domain/auth/repositories.py
- [X] T009 Implementar repositorios SQLite transaccionales de autenticación en backend/src/baku/backend/infrastructure/persistence/sqlite/auth_repositories.py
- [X] T010 Crear migración SQLite para tablas de operador, token revocado y throttle en backend/migrations/versions/0001_f0001_auth_tables.py
- [X] T011 [P] Implementar utilitario de reloj UTC para timestamps de auth y auditoría en backend/src/baku/backend/application/common/utc_clock.py
- [X] T039 Implementar middleware de extracción y propagación de correlation_id en requests entrantes en backend/src/baku/backend/interfaces/http/middleware/correlation_id.py
- [X] T012 Implementar mapeador HTTP de errores tipificados de auth con correlation_id (requiere T039) en backend/src/baku/backend/interfaces/http/error_mapper.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Bootstrap de credenciales iniciales (Priority: P1) 🎯 MVP

**Goal**: Permitir establecer las credenciales del operador único en el primer arranque y rechazar cualquier intento de repetición

**Independent Test**: En base de datos limpia, el bootstrap responde 201; un segundo intento responde 409 con `AUTH_BOOTSTRAP_ALREADY_COMPLETED` y `correlation_id`.

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T013 [P] [US1] Crear contract test de POST /api/v1/auth/bootstrap (201 y 409) en backend/tests/contract/auth/test_bootstrap_contract.py
- [X] T014 [P] [US1] Crear integración de bootstrap único y rechazo de repetición en backend/tests/integration/auth/test_bootstrap_flow.py

### Implementation for User Story 1

- [X] T015 [P] [US1] Implementar DTOs BootstrapRequest y respuesta de bootstrap en backend/src/baku/backend/interfaces/http/api/v1/schemas/auth_bootstrap.py
- [X] T016 [US1] Implementar caso de uso BootstrapOperator con hash de contraseña y creación de Operator en backend/src/baku/backend/application/auth/bootstrap_operator.py
- [X] T017 [US1] Implementar endpoint POST /api/v1/auth/bootstrap en backend/src/baku/backend/interfaces/http/api/v1/auth_router.py
- [X] T040 [US1] Registrar auth_router en el entry point de la aplicación FastAPI en backend/src/baku/backend/main.py
- [X] T018 [US1] Registrar mapeo de error AUTH_BOOTSTRAP_ALREADY_COMPLETED → 409 en backend/src/baku/backend/interfaces/http/error_mapper.py

**Checkpoint**: US1 completa y verificable de forma independiente

---

## Phase 4: User Story 2 - Inicio y cierre de sesión (Priority: P1)

**Goal**: Autenticar al operador emitiendo JWT con expiración configurable, proteger rutas y revocar token actual en logout

**Independent Test**: Login con credenciales válidas devuelve token usable en ruta protegida; credenciales inválidas devuelven 401; N intentos fallidos consecutivos activan bloqueo 429; logout revoca el token y su reutilización devuelve 401.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T019 [P] [US2] Crear contract tests de POST /api/v1/auth/login y POST /api/v1/auth/logout en backend/tests/contract/auth/test_login_logout_contract.py
- [X] T020 [P] [US2] Crear integración de flujo login exitoso, fallo, logout con revocación por jti e idempotencia de doble logout (reintento con token ya revocado devuelve 401) en backend/tests/integration/auth/test_login_logout_flow.py
- [X] T021 [P] [US2] Crear integración de bloqueo temporal por intentos fallidos configurables en backend/tests/integration/auth/test_login_lockout_flow.py

### Implementation for User Story 2

- [X] T022 [P] [US2] Implementar hasher/verificador de contraseñas no reversibles en backend/src/baku/backend/infrastructure/security/password_hasher.py
- [X] T023 [P] [US2] Implementar servicio JWT con claims sub, ver, jti y exp en backend/src/baku/backend/infrastructure/security/jwt_service.py
- [X] T024 [US2] Implementar caso de uso LoginOperator con throttle, last_login_at y emisión de token en backend/src/baku/backend/application/auth/login_operator.py
- [X] T025 [US2] Implementar caso de uso LogoutOperator con persistencia de RevokedToken en backend/src/baku/backend/application/auth/logout_operator.py
- [X] T026 [US2] Implementar endpoints POST /api/v1/auth/login y POST /api/v1/auth/logout en backend/src/baku/backend/interfaces/http/api/v1/auth_router.py
- [X] T027 [US2] Implementar dependencia de autenticación para rutas protegidas (validación JWT + revocación) en backend/src/baku/backend/interfaces/http/dependencies/require_auth.py
- [X] T028 [US2] Registrar mapeo de errores AUTH_INVALID_CREDENTIALS, AUTH_LOCKED_TEMPORARILY, AUTH_TOKEN_INVALID, AUTH_TOKEN_EXPIRED y AUTH_TOKEN_REVOKED en backend/src/baku/backend/interfaces/http/error_mapper.py
- [X] T041 [US2] Registrar mapeo de errores AUTH_FORBIDDEN → 403 y AUTH_PASSWORD_CHANGE_REQUIRES_AUTH → 401 en backend/src/baku/backend/interfaces/http/error_mapper.py

**Checkpoint**: US2 completa y verificable de forma independiente

---

## Phase 5: User Story 3 - Rotación de contraseña con revocación global (Priority: P1)

**Goal**: Permitir cambio de contraseña autenticado que incremente credential_version y revoque inmediatamente todos los tokens previos

**Independent Test**: Tras cambio de contraseña, tokens emitidos antes son rechazados por desajuste de ver; login con credenciales nuevas emite tokens válidos.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T029 [P] [US3] Crear contract test de PUT /api/v1/auth/password (204 y 401) en backend/tests/contract/auth/test_password_change_contract.py
- [X] T030 [P] [US3] Crear integración de rotación de contraseña y revocación global por ver en backend/tests/integration/auth/test_password_rotation_flow.py

### Implementation for User Story 3

- [X] T031 [US3] Implementar caso de uso ChangeOperatorPassword con incremento atómico de credential_version en backend/src/baku/backend/application/auth/change_operator_password.py
- [X] T032 [US3] Implementar endpoint PUT /api/v1/auth/password en backend/src/baku/backend/interfaces/http/api/v1/auth_router.py
- [X] T033 [US3] Aplicar validación del claim ver contra credential_version persistido en backend/src/baku/backend/interfaces/http/dependencies/require_auth.py
- [X] T034 [US3] Persistir updated_at únicamente en modificación efectiva del operador en backend/src/baku/backend/infrastructure/persistence/sqlite/auth_repositories.py

**Checkpoint**: US3 completa y verificable de forma independiente

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de consistencia contractual, documental y de calidad

- [X] T035 [P] Actualizar auth-api-v1.yaml para reflejar responses reales de implementación y ejecutar validación de schema OpenAPI en specs/001-acceso-autenticacion-operador/contracts/auth-api-v1.yaml
- [X] T036 [P] Verificar que todos los error_code emitidos en error_mapper.py están documentados en error-model.md y actualizar si hay divergencia en specs/001-acceso-autenticacion-operador/contracts/error-model.md
- [X] T037 [P] Ejecutar flujo completo de quickstart.md (bootstrap→login→logout→rotación→bloqueo) y documentar resultado de validación manual en specs/001-acceso-autenticacion-operador/quickstart.md
- [X] T038 Documentar ejecución local de gates de calidad (lint, type-check, tests, contracts) en backend/README.md
- [X] T042 Declarar explícitamente en specs/001-acceso-autenticacion-operador/spec.md que SC-004 (p95 < 2s) es objetivo operativo no automatizado en MVP; añadir nota de benchmark como mejora post-MVP
- [X] T043 [P] Añadir verificación de ausencia de cross-root imports entre backend y bot al pipeline de CI en .github/workflows/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - sin dependencias en otras historias
- **User Story 2 (P1)**: Depends on US1 (requiere Operator existente para login real)
- **User Story 3 (P1)**: Depends on US2 (requiere sesión autenticada y JWT emitido)

### Dependency Graph

- US1 → US2 → US3

### Within Each User Story

- Contract tests e integration tests ANTES de implementación (deben fallar primero)
- DTOs y entidades antes que casos de uso
- Casos de uso antes que endpoints
- Endpoints antes que registro de errores y dependencias de autenticación

---

## Parallel Opportunities

- **Setup**: T002, T003, T004a, T004b en paralelo tras T001
- **Foundational**: T006, T007 y T011 en paralelo; T039 antes de T012
- **US1**: T013, T014 y T015 en paralelo
- **US2**: T019, T020, T021, T022 y T023 en paralelo
- **US3**: T029 y T030 en paralelo
- **Polish**: T035, T036 y T037 en paralelo

## Parallel Example: User Story 2

```bash
# Pruebas de US2 en paralelo (deben fallar antes de implementar):
Task: "Crear contract tests de login/logout en backend/tests/contract/auth/test_login_logout_contract.py"
Task: "Crear integración de login/logout en backend/tests/integration/auth/test_login_logout_flow.py"
Task: "Crear integración de bloqueo temporal en backend/tests/integration/auth/test_login_lockout_flow.py"

# Infrestructura de seguridad en paralelo:
Task: "Implementar hasher de contraseñas en backend/src/baku/backend/infrastructure/security/password_hasher.py"
Task: "Implementar servicio JWT en backend/src/baku/backend/infrastructure/security/jwt_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: verificar bootstrap exitoso y rechazo de repetición
5. Deploy/demo si listo

### Incremental Delivery

1. US1: Bootstrap único → operador registrado y sistema protegido
2. US2: Login/logout + throttle → acceso diario habilitado
3. US3: Rotación de contraseña + revocación global → ciclo de seguridad completo
4. Polish: contratos y documentación sincronizados

### Parallel Team Strategy

1. Team completa Setup + Foundational juntos
2. Luego:
   - Developer A: US1 (bootstrap)
   - Developer B: US2 (login/logout/throttle) una vez US1 en PR
   - Developer C: US3 (password rotation) una vez US2 en PR

---

## Notes

- Todas las tareas siguen formato checklist ejecutable con ID secuencial, etiquetas y ruta absoluta de archivo
- Implementación concentrada en root `backend` respetando ADR-0001 (sin cross-root imports)
- Si durante implementación cambia comportamiento o contrato, actualizar `specs/001-acceso-autenticacion-operador/` en el mismo PR (SDD)
- Mapeado de ADR activos: ADR-0003 (SQLite/transacciones), ADR-0004 (HTTP v1), ADR-0005 (JWT+ver), ADR-0006 (contract tests), ADR-0008 (CI gates), ADR-0009 (errores tipificados), ADR-0012 (UTC)
