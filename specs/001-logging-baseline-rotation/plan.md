# Implementation Plan: EN-0200 Application Logging Baseline with Daily Rotation

**Branch**: `001-logging-baseline-rotation` | **Date**: 2026-03-07 | **Spec**: `specs/001-logging-baseline-rotation/spec.md`
**Input**: Feature specification from `specs/001-logging-baseline-rotation/spec.md`

## Summary

Implementar un baseline transversal de observabilidad para `backend/` que unifique logs
estructurados con doble salida (JSON + human-friendly), rotacion diaria a las 00:00
Europe/Madrid, retencion inicial de 7 dias para logs rotados (configurable por entorno)
y conservacion de ficheros activos,
configuracion dedicada por entorno (`dev`, `test`, `prod`) en perfiles del framework en
la raiz de `backend/`. El plan preserva arquitectura hexagonal, no cambia contratos externos y alinea
la documentacion funcional existente para integrar EN-0200 en todas las features
documentadas.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, SQLAlchemy, PyJWT, bcrypt, python-dotenv, stdlib logging  
**Storage**: SQLite para datos de negocio (sin cambios de esquema); ficheros para logs operativos  
**Testing**: pytest, integration tests backend, contract tests existentes, ruff, mypy  
**Target Platform**: Linux self-hosted en LAN (incluido hardware limitado)  
**Project Type**: Backend web-service en monorepo multi-root  
**Performance Goals**: continuidad operativa del logging durante rotacion y trazabilidad consistente por `correlation_id`  
**Constraints**: sin acoplar Domain a infraestructura, sin cambios de contrato HTTP/eventos, configuracion del framework de logging externa y sin configuracion embebida en codigo  
**Scale/Scope**: alcance exclusivo `backend/`; impacto documental transversal en `docs/spec/features/`

## Dependency Graph Check

- Item objetivo: `EN-0200` (`planned`, `MVP0`).
- Dependencia declarada: `EN-0202` (`done`) -> satisfecha.
- Orden DAG: EN-0200 antecede dependencias posteriores (`EN-0208` via cadena de MVP2).
- El plan no requiere items posteriores para implementacion base del enabler.

Dependency Graph Issue: None.

## Impacto de Enabler sobre Features Existentes

- Dependencia transitiva detectada por DAG: `F-0014` (`F-0014` -> `EN-0208` -> `EN-0200`).
- Alineacion definida en la especificacion clarificada: actualizacion documental de todas
  las features existentes bajo `docs/spec/features/` para integrar baseline de
  observabilidad cuando aplique, sin cambiar alcance funcional de cada feature.

## Shared Constitution Checklist Template

Usar este bloque como fuente unica para los checks constitucionales de pre y post diseno,
evitando divergencia entre secciones.

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

- `ADR-0002` (Hexagonal): logging como concern transversal en adapters/infrastructure sin
  contaminar Domain.
- `ADR-0009` (Error model and observability): campos obligatorios, correlacion,
  persistencia de logs y exclusion de datos sensibles.
- `ADR-0012` (Time policy): timestamp de eventos en UTC con rotacion operativa en
  Europe/Madrid.
- `ADR-0013` (Configuration system): carga de configuracion externa de runtime,
  incluyendo referencia al fichero de perfil del framework de logging por entorno.
- `ADR-0001` y `ADR-0006`: sin coupling cross-root y sin nuevos contratos externos.
- `ADR-0008`: quality gates obligatorios en CI para cambios funcionales.

ADR Gap: None.

## Phase 0 - Research Output

Archivo: `specs/001-logging-baseline-rotation/research.md`

Resultados consolidados:
- Doble salida obligatoria (JSON + human-friendly) para mismo evento logico.
- Retencion definida sin ambiguedad: valor inicial 7 dias para logs rotados,
  configurable por entorno, mas ficheros activos.
- Configuracion del framework de logging dedicada por entorno (`dev`, `test`, `prod`),
  en ficheros externos en la raiz de `backend/`, con fallback seguro si un perfil no es
  cargable.
- Confirmado: sin cambios de contratos HTTP/eventos y sin ADR nuevo.

## Phase 1 - Design & Contracts

### Data Model

Archivo: `specs/001-logging-baseline-rotation/data-model.md`

Artefacto de diseno:
- `Logging Framework Configuration File (per environment)` como artefacto de
  configuracion operacional (sin modelo de datos de dominio adicional)

### Contracts

Archivo: `specs/001-logging-baseline-rotation/contracts/no-contract-changes.md`

Decision: no hay cambios en contratos HTTP/eventos; sin impacto de versionado externo.

### Quickstart

Archivo: `specs/001-logging-baseline-rotation/quickstart.md`

Incluye validacion de:
- Arranque correcto cargando perfil dedicado del framework de logging por entorno desde la raiz de `backend/`.
- Fallback seguro del framework con baseline minimo obligatorio de logging si fichero requerido falta o es invalido (sin modo "sin logging").
- Contrato de fallback por entorno con escritura en consola (`dev` human-friendly, `test` human-friendly minimalista, `prod` JSON estructurado).
- Correlacion y campos obligatorios en doble salida.
- Rotacion 00:00 Europe/Madrid y retencion en dias (default 7) configurable por entorno.
- Continuidad/integridad antes y despues de rotacion, con asercion explicita de no perdida de eventos relevantes.

## Post-Design Constitution Check

Checklist reference: `Shared Constitution Checklist Template`.

- [x] All checklist items pass at post-design gate.

Gate Status: PASS

## Architectural Impact Assessment

- HTTP contracts: no changes.
- Events: no changes.
- Persistence: sin migraciones de DB; si hay persistencia operativa en fichero de logs.
- Configuration: cambio material (ficheros dedicados por entorno + parametros de logging).
- Error model: sin cambio de contrato externo; se refuerza observabilidad tecnica.
- Versioning impact: none (sin superficie contractual externa modificada).

## Project Structure

### Documentation (this feature)

```text
specs/001-logging-baseline-rotation/
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
│           │   └── config/
│           ├── interfaces/
│           │   └── http/
│           └── main.py
└── tests/
    ├── contract/
    └── integration/

docs/
└── spec/
    └── features/
```

**Structure Decision**: Se mantiene estructura multi-root existente; implementacion tecnica
limitada a `backend/` y sincronizacion documental en `docs/spec/features/`.

## CI and Quality Gates

- Lint: `ruff`.
- Static typing: `mypy`.
- Tests: `pytest` (incluyendo integracion relevantes a observabilidad).
- Contract tests: ejecutar suite existente para confirmar no-regresion.
- Validaciones especificas EN-0200: carga de perfiles de logging por entorno, fallback seguro, campos obligatorios,
  correlacion, rotacion y retencion.

## Documentation Synchronization

Actualizar durante implementacion:
- `README.md`
- `backend/README.md`
- `docs/spec/features/*.md` (features existentes)

Actualizar solo si cambia estado del item:
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

Estados permitidos: `planned`, `in_progress`, `done`.

## Complexity Tracking

No constitution violations identified. No complexity waiver required.

## Implementation Validation Evidence

- `ruff check src tests` -> pass (All checks passed).
- `C:/python/venvs/baku-casa/backend/Scripts/python.exe -m mypy src` -> pass (no issues in 65 source files).
- `PYTHONPATH=src pytest -q` -> pass (`76 passed, 4 warnings`).
- Contract regression suite:
  - `backend/tests/contract/auth/test_bootstrap_contract.py` -> pass
  - `backend/tests/contract/auth/test_login_logout_contract.py` -> pass
  - `backend/tests/contract/auth/test_password_change_contract.py` -> pass
