# Implementation Plan: EN-0201 In-Memory Database Testing Baseline

**Branch**: `001-inmemory-db-testing` | **Date**: 2026-03-07 | **Spec**: `specs/001-inmemory-db-testing/spec.md`
**Input**: Feature specification from `specs/001-inmemory-db-testing/spec.md`

## Summary

Implementar un baseline de pruebas de integración con persistencia en memoria para `backend/`, con inicialización de esquema determinista, aislamiento entre pruebas y configuración de testing explícita separada de runtime normal, compatible con ejecución local y CI y sin dependencias externas adicionales.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, SQLAlchemy, pytest, tooling de calidad (`ruff`, `mypy`)  
**Storage**: SQLite en memoria para pruebas de integración; SQLite persistente fuera del contexto de testing  
**Testing**: pytest (unit + integration + contract)  
**Target Platform**: Linux self-hosted y entorno local de desarrollo  
**Project Type**: Backend web-service en monorepo multi-root  
**Performance Goals**: Reducir tiempo de feedback de integración y mantener reproducibilidad determinista  
**Constraints**: Sin dependencias externas para pruebas con DB, sin alterar runtime normal, sin romper límites hexagonales  
**Scale/Scope**: Alcance exclusivo `backend/` y suites de pruebas de integración con persistencia

## Dependency Graph Check

- Item objetivo: `EN-0201` (`planned`, `MVP0`).
- Dependencia declarada: `EN-0202` (`done`) -> satisfecha.
- Orden DAG: EN-0201 no depende de items posteriores.
- No se detectan dependencias implícitas nuevas para este plan.

Dependency Graph Issue: None.

## Impacto de Enabler sobre Features Existentes

- Revisión de dependencias directas/transitivas desde `docs/spec/dependency-graph.yaml`: no hay features existentes que dependan explícitamente de `EN-0201` en el DAG actual.
- Aplicación práctica del baseline: al estar marcado `affects_future_features: true`, las features de `backend` deben asumir EN-0201 en implementación y validación de persistencia cuando aplique.

## Shared Constitution Checklist Template

Usar este bloque como fuente única para los checks constitucionales de pre y post diseño.

- [ ] Layer boundaries preserved (Domain/Application/Interfaces/Infrastructure)
- [ ] No cross-root runtime coupling introduced; integration only through versioned contracts
- [ ] Contract impact classified (breaking/non-breaking) and versioning impact declared
- [ ] Typed error mapping and stable error codes defined for new failure modes
- [ ] Financial/time invariants respected (Decimal-only money, percentage 0-100, UTC aware datetime)
- [ ] TDD strategy declared (red -> green -> refactor) for functional changes
- [ ] Contract tests included when any contract surface changes
- [ ] Spec updates identified for behavior changes
- [ ] ADR updates/new ADR identified for structural or architectural changes
- [ ] CI quality gates impacted by this feature are listed (lint, type-check, tests, contracts)

## Constitution Check (Pre-Design Gate)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Checklist reference: `Shared Constitution Checklist Template`.

- [x] All checklist items pass at pre-design gate.

Gate Status: PASS

## ADR Alignment

- `ADR-0002` (Hexagonal): pruebas de persistencia aisladas sin mover lógica de negocio fuera de Domain/Application.
- `ADR-0003` (Persistence): baseline explícito de integración sobre SQLite en memoria para tests, manteniendo runtime persistente fuera de test.
- `ADR-0008` (CI/Governance): integración de pruebas reproducibles en quality gates.
- `ADR-0013` (Configuration): configuración de testing explícita, centralizada y separada de runtime normal.
- `ADR-0001` y `ADR-0006`: sin coupling runtime entre roots ni cambios de contratos entre componentes.
- `ADR-0012`: sin cambio de semántica temporal de dominio; timestamps y reglas UTC se mantienen.

ADR Gap: None.

## Phase 0 - Research Output

Archivo: `specs/001-inmemory-db-testing/research.md`

Resultados consolidados:
- Configuración de testing separada y activación explícita.
- Inicialización determinista de esquema para integración con DB.
- Aislamiento garantizado entre tests con política consistente de limpieza/rollback/recreación.
- Convenciones de clasificación y ubicación de pruebas de integración con persistencia.
- Compatibilidad reproducible en local y CI sin dependencias externas.

## Phase 1 - Design & Contracts

### Data Model

Archivo: `specs/001-inmemory-db-testing/data-model.md`

No aplica modelo de dominio nuevo. Se documenta únicamente el artefacto de configuración de testing con DB en memoria y las reglas de ciclo de vida del esquema para pruebas.

### Contracts

Archivo: `specs/001-inmemory-db-testing/contracts/no-contract-changes.md`

Decisión: no hay cambios en contratos HTTP/eventos; sin impacto de versionado externo.

### Quickstart

Archivo: `specs/001-inmemory-db-testing/quickstart.md`

Incluye validación de:
- Activación explícita del baseline de testing con DB en memoria.
- Inicialización determinista de esquema para pruebas.
- Aislamiento entre tests y ausencia de estado compartido.
- Ejecución reproducible local/CI y sin dependencias externas.

## Post-Design Constitution Check

Checklist reference: `Shared Constitution Checklist Template`.

- [x] All checklist items pass at post-design gate.

Gate Status: PASS

## Architectural Impact Assessment

- HTTP contracts: no changes.
- Events: no changes.
- Persistence: changed (capacidad de testing en memoria + esquema determinista para integración).
- Configuration: changed (perfil de testing explícito y separado).
- Error model: no changes contractuales.
- Versioning impact: none.

## Project Structure

### Documentation (this feature)

```text
specs/001-inmemory-db-testing/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── no-contract-changes.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   └── baku/
│       └── backend/
│           ├── application/
│           ├── domain/
│           ├── infrastructure/
│           ├── interfaces/
│           └── main.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

docs/
└── spec/
    └── features/
```

**Structure Decision**: Se mantiene estructura multi-root actual; EN-0201 afecta únicamente `backend/` y su disciplina de pruebas.

## CI and Quality Gates

- Lint: `ruff`.
- Static typing: `mypy`.
- Tests: `pytest` con foco en suites de integración con DB en memoria.
- Contract tests: ejecución de regresión para confirmar ausencia de cambios contractuales.

### EN-0201 Execution Evidence

- `python -m ruff check src tests`: PASS.
- `python -m mypy src`: no ejecutable en el entorno actual (`No module named mypy`).
- `pytest tests/integration/persistence tests/integration/configuration/test_persistence_test_profile_activation.py tests/integration/configuration/test_runtime_db_profile_isolation.py tests/integration/configuration/test_test_db_url_precedence.py`: PASS (8 passed).
- `pytest tests/contract/auth/test_bootstrap_contract.py tests/contract/auth/test_login_logout_contract.py tests/contract/auth/test_password_change_contract.py`: PASS (13 passed).

## Documentation Synchronization

Actualizar durante implementación:
- `backend/README.md`
- `README.md`
- Features existentes en `docs/spec/features/` cuando aplique referencia a baseline de testing con DB.

Actualizar solo si cambia estado del item:
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

Estados permitidos: `planned`, `in_progress`, `done`.

## Complexity Tracking

No constitution violations identified. No complexity waiver required.
