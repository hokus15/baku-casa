# Implementation Plan: EN-0300 HTTP Application Bootstrap Modularization

**Branch**: `001-http-bootstrap-modularization` | **Date**: 2026-03-07 | **Spec**: `specs/001-http-bootstrap-modularization/spec.md`
**Input**: Feature specification from `specs/001-http-bootstrap-modularization/spec.md`

## Summary

Implementar una reorganizacion estructural del bootstrap HTTP del root `backend/` para separar responsabilidades de inicializacion, mantener el composition root como unico punto de composicion de dependencias entre capas y preservar comportamiento externo sin cambios contractuales. El plan mantiene fail-fast ante errores criticos de arranque y exige quality gates minimos (lint, type-check, regresion funcional/contractual cuando aplique).

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, SQLAlchemy, PyJWT, python-dotenv  
**Storage**: SQLite (sin cambios de esquema en EN-0300)  
**Testing**: pytest, contract regression existente, quality gates con ruff y mypy  
**Target Platform**: Linux self-hosted y entorno local de desarrollo  
**Project Type**: backend web-service en monorepo multi-root  
**Performance Goals**: mantener equivalencia funcional y de arranque (sin degradacion silenciosa)  
**Constraints**: sin cambios en contratos HTTP/eventos, sin cambios de dominio, sin coupling entre roots, fail-fast en bootstrap critico  
**Scale/Scope**: alcance exclusivo `backend/` sobre bootstrap HTTP y composicion de dependencias

## Dependency Graph Check

- Item objetivo: `EN-0300` (`planned`, `MVP0`).
- Dependencia declarada: `EN-0202` (`done`) -> satisfecha.
- Orden DAG: no requiere features/enablers posteriores para su implementacion.
- Dependencias implicitas nuevas: no detectadas.

Dependency Graph Issue: None.

## Impacto de Enabler sobre Features Existentes

- Analisis sobre `docs/spec/dependency-graph.yaml`: no existe feature documentada en `docs/spec/features/` con dependencia directa o transitiva declarada hacia `EN-0300` en el estado actual del DAG.
- Implicacion futura: por `affects_future_features: true`, las features futuras de `backend` que usen bootstrap HTTP deben asumir este baseline estructural.

## Constitution Check (Pre-Design Gate)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Layer boundaries preserved (Domain/Application/Interfaces/Infrastructure)
- [x] No cross-root runtime coupling introduced; integration only through versioned contracts
- [x] Contract impact classified (breaking/non-breaking) and versioning impact declared
- [x] Typed error mapping and stable error codes defined for new failure modes
- [x] Financial/time invariants respected (Decimal-only money, percentage 0-100, UTC aware datetime)
- [x] TDD strategy declared (red -> green -> refactor) for functional changes
- [x] Contract tests included when any contract surface changes
- [x] Spec updates identified for behavior changes
- [x] ADR updates/new ADR identified for structural or architectural changes
- [x] CI quality gates impacted by this feature are listed (lint, type-check, tests, contracts)

Gate Status: PASS

## ADR Alignment

- `ADR-0002` (Hexagonal): composicion de dependencias permanece centralizada en composition root; sin fuga de responsabilidades a Domain/Application.
- `ADR-0004` (HTTP/OpenAPI): se reorganiza arranque HTTP sin alterar contratos ni versionado.
- `ADR-0006` (Contract discipline): no hay cambios contractuales; se ejecuta regresion para confirmar no impacto.
- `ADR-0008` (Governance): quality gates minimos explicitos y obligatorios para cerrar EN-0300.
- `ADR-0013` (Configuration): se preserva el comportamiento fail-fast ante errores criticos de inicializacion.

ADR Gap: None.

## Phase 0 - Research Output

Archivo: `specs/001-http-bootstrap-modularization/research.md`

Resultados consolidados:
- Definicion de limites de responsabilidad del entrypoint HTTP y del bootstrap modularizado.
- Estrategia de preservacion del composition root unico para composicion de dependencias.
- Criterios de preservacion de fail-fast y trazabilidad de errores de bootstrap.
- Alcance minimo de quality gates para cerrar el enabler sin cambios contractuales.

## Phase 1 - Design & Contracts

### Data Model

Archivo: `specs/001-http-bootstrap-modularization/data-model.md`

No aplica modelo de dominio nuevo. Se documentan artefactos estructurales de bootstrap (no funcionales) y sus reglas de validacion.

### Contracts

Archivo: `specs/001-http-bootstrap-modularization/contracts/no-contract-changes.md`

Decision: no hay cambios en contratos HTTP/eventos; impacto de versionado externo: none.

### Quickstart

Archivo: `specs/001-http-bootstrap-modularization/quickstart.md`

Incluye validacion de:
- Entry point acotado y responsabilidades de bootstrap separadas.
- Composition root unico para wiring de dependencias entre capas.
- Fail-fast en errores criticos de bootstrap.
- Regresion funcional/contractual y quality gates minimos.

## Post-Design Constitution Check

- [x] Layer boundaries preserved (Domain/Application/Interfaces/Infrastructure)
- [x] No cross-root runtime coupling introduced; integration only through versioned contracts
- [x] Contract impact classified (breaking/non-breaking) and versioning impact declared
- [x] Typed error mapping and stable error codes defined for new failure modes
- [x] Financial/time invariants respected (Decimal-only money, percentage 0-100, UTC aware datetime)
- [x] TDD strategy declared (red -> green -> refactor) for functional changes
- [x] Contract tests included when any contract surface changes
- [x] Spec updates identified for behavior changes
- [x] ADR updates/new ADR identified for structural or architectural changes
- [x] CI quality gates impacted by this feature are listed (lint, type-check, tests, contracts)

Gate Status: PASS

## Architectural Impact Assessment

- HTTP contracts: no changes.
- Events: no changes.
- Persistence: no changes.
- Configuration: no changes contractuales; se mantiene fail-fast de bootstrap.
- Error model: no changes contractuales; se mantiene trazabilidad.
- Versioning impact: none.

## Project Structure

### Documentation (this feature)

```text
specs/001-http-bootstrap-modularization/
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
```

**Structure Decision**: Se mantiene la estructura multi-root actual; EN-0300 afecta exclusivamente el bootstrap HTTP del root `backend/`.

## CI and Quality Gates

- Lint: `ruff`.
- Type-check: `mypy`.
- Tests: `pytest` (regresion funcional relevante).
- Contract regression: ejecutar suite contractual cuando aplique para confirmar ausencia de cambios de superficie.

### Quality Gate Evidence (EN-0300, 2026-03-07)

| Gate | Result | Detail |
|------|--------|--------|
| `ruff check src/ tests/` | ✅ PASS | All checks passed |
| `mypy src/` | ✅ PASS | Success: no issues found in 73 source files |
| `pytest tests/` | ✅ PASS | 121 passed, 0 failed, 3 warnings (pre-existing) |
| Contract regression | ✅ PASS | Contract tests included in full suite (121 tests) |

Bootstrap integration test suite: **37 new tests**, all passing.

## Documentation Synchronization

Actualizar durante implementacion:
- `backend/README.md`.
- `README.md`.
- Features existentes en `docs/spec/features/` solo si pasan a depender explicitamente de EN-0300 en el DAG.

Actualizar solo si cambia estado del item:
- `docs/spec/roadmap.md`.
- `docs/spec/dependency-graph.yaml`.

Estados permitidos: `planned`, `in_progress`, `done`.

## Complexity Tracking

No constitution violations identified. No complexity waiver required.
