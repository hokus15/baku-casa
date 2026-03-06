# Implementation Plan: EN-0202 Configuration System

**Branch**: `001-configuration-system` | **Date**: 2026-03-06 | **Spec**: `specs\001-configuration-system\spec.md`
**Input**: Feature specification from `specs\001-configuration-system\spec.md`

## Summary

Implementar una capacidad transversal de configuracion tipada y centralizada para
`backend/`, con resolucion determinista multi-fuente (`environment variables > config file
> defaults`), validacion fail-fast en arranque, reporte agregado de errores y warnings
diagnosticos para claves no declaradas; todo sin cambios de contrato externo. El alcance
incluye consolidar bajo EN-0202 la configuracion preexistente consumida por `F-0001`
(autenticacion) preservando su comportamiento funcional.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, SQLAlchemy, PyJWT, bcrypt, python-dotenv (backend root)  
**Storage**: SQLite (sin cambios de esquema para este item)  
**Testing**: pytest, integration tests con SQLite en memoria, mypy, ruff  
**Target Platform**: Linux self-hosted (LAN), hardware limitado (incl. Raspberry Pi)  
**Project Type**: Backend web-service dentro de monorepo multi-root  
**Performance Goals**: Arranque determinista y validacion temprana de configuracion; sin
objetivo de throughput nuevo para este item  
**Constraints**: Sin acoplamiento a Domain; sin cambios de contrato HTTP/eventos; sin
dependencias externas gestionadas; CI obligatoria en verde  
**Scale/Scope**: Alcance exclusivo `backend/` como enabler de MVP0 para capacidades
posteriores (`EN-0200`, `EN-0201`, `EN-0300`)

## Dependency Graph Check

- `EN-0202` depende de `F-0001`; dependencia satisfecha (`done`).
- El orden de implementacion respeta DAG (`EN-0202` antecede a `EN-0200`, `EN-0201`,
  `EN-0300`).
- No se detectan dependencias implicitas adicionales.

Dependency Graph Issue: None.

## Dependency Integration with F-0001

- `F-0001` es prerequisito directo de `EN-0202`; por tanto EN-0202 MUST incorporar y
    normalizar las claves de configuracion ya usadas por autenticacion.
- Este plan incluye compatibilidad explicita para parametros configurables de `F-0001`
    (ej. TTL de token y politica de bloqueo por intentos) sin alterar semantica de negocio
    definida en la feature.
- Cualquier cambio de nombre o estructura de claves MUST contemplar estrategia de
    transicion y documentacion para evitar ruptura operativa.

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

- ADR-0013 (Configuration System): regla central de diseno y precedencia.
- ADR-0002 (Hexagonal): Domain sin dependencias de configuracion.
- ADR-0001 (Multi-root): alcance solo `backend/`, sin imports cross-root.
- ADR-0007 (Delivery): configuracion compatible con self-hosted y secretos en runtime.
- ADR-0008 (Governance): pruebas y quality gates requeridas en CI.

ADR Gap: None.

## Phase 0 - Research Output

Archivo: `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\specs\001-configuration-system\research.md`

Resultados consolidados:
- Precedencia global fija validada.
- Politica de claves no declaradas (warning, no bloqueo) fijada.
- Error handling de validacion agregado (fallo con conjunto completo).
- Segmentacion por entorno con requeridos globales (sin minimos por entorno).
- Confirmado: sin cambios de contrato externo y sin ADR nuevo.

## Phase 1 - Design & Contracts

### Data Model

Archivo: `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\specs\001-configuration-system\data-model.md`

Entidades de diseno:
- `ConfigurationParameterDefinition`
- `ConfigurationSourceInput`
- `ResolvedConfigurationProfile`
- `ConfigurationValidationIssue`

### Contracts

Archivo: `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\specs\001-configuration-system\contracts\no-contract-changes.md`

Decision: no hay cambios en contratos HTTP/eventos; sin impacto de versionado externo.

### Quickstart

Archivo: `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\specs\001-configuration-system\quickstart.md`

Incluye validacion de:
- Precedencia determinista.
- Fallo fail-fast con errores agregados.
- Warnings por claves no declaradas.
- Aislamiento de perfil `test`.

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

## Impact Assessment

- HTTP contracts: no changes.
- Events: no changes.
- Persistence: no schema migration required by this item.
- Configuration: changed (capacidad transversal nueva).
- Error model: changed (errores tipificados de configuracion internos).
- Versioning impact: none (sin contratos externos modificados).

Impact on existing F-0001 configuration: explicit and in-scope (normalizacion y
centralizacion sin cambio funcional de autenticacion).

## Project Structure

### Documentation (this feature)

```text
specs/001-configuration-system/
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
    ├── contract/
    └── integration/

bot/
└── (no changes for EN-0202)
```

**Structure Decision**: Se aplica estructura multi-root existente; el alcance de
implementacion es exclusivo de `backend/`.

## CI and Quality Gates

- Lint: ruff.
- Static typing: mypy.
- Tests: unit/integration relevantes a configuracion.
- Regression tests: validacion de no-regresion de configuracion consumida por `F-0001`.
- Contract tests: no obligatorios para este item (sin cambio de superficie contractual).
- Build/compose validation: sin cambios estructurales requeridos por EN-0202.

### Quality Gate Results (2026-03-06)

| Gate | Result | Details |
|---|---|---|
| `ruff check src/ tests/` | ✅ PASS | All checks passed |
| `mypy src/ --ignore-missing-imports` | ✅ PASS | No issues in 60 source files |
| `pytest tests/` | ✅ PASS | 64 passed, 0 failed (30 new EN-0202 tests + 34 F-0001 regression) |

## Documentation Synchronization

Actualizar durante implementacion:
- `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\README.md`
- `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\backend\README.md`

Actualizar solo si cambia estado del item:
- `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\docs\spec\roadmap.md`
- `c:\Users\hokus\OneDrive\Documentos\GitHub\baku-casa\docs\spec\dependency-graph.yaml`

## Complexity Tracking

No constitution violations identified. No complexity waiver required.
