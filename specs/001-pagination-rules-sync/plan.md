# Implementation Plan: Alineacion de reglas de paginacion en F-0001/F-0002/F-0003

**Branch**: `001-pagination-rules-sync` | **Date**: 2026-03-11 | **Spec**: `specs/001-pagination-rules-sync/spec.md`
**Input**: Feature specification from `specs/001-pagination-rules-sync/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Sincronizar el comportamiento esperado de listados y busquedas en F-0001, F-0002 y F-0003 para que la paginacion sea obligatoria y totalmente gobernada por EN-0202 (fuente central de configuracion y precedencia `environment variables > config file > defaults`). La implementacion se limita a actualizacion de especificaciones funcionales, validaciones de consistencia contractual y cobertura de pruebas de contrato/integacion donde aplique, sin introducir nuevas capacidades de dominio ni cambios de arquitectura.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11 (backend)  
**Primary Dependencies**: FastAPI/OpenAPI (ADR-0004), SQLAlchemy/SQLite (ADR-0003), centralized typed configuration (ADR-0013)  
**Storage**: SQLite (sin cambios de esquema)  
**Testing**: pytest (unit/integration/contract), con baseline EN-0201 donde aplique  
**Target Platform**: backend self-hosted en contenedores (ADR-0007)
**Project Type**: monorepo multi-root, foco en web-service backend (ADR-0001)  
**Performance Goals**: evitar colecciones no acotadas y mantener respuesta paginada consistente en endpoints de lista/busqueda  
**Constraints**: no cambios funcionales fuera de alcance; sin migraciones; sin rutas absolutas; sin contradiccion con ADR  
**Scale/Scope**: 3 especificaciones de feature existentes (F-0001, F-0002, F-0003) y artefactos de documentacion/contrato asociados

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Layer boundaries preserved (Domain/Application/Interfaces/Infrastructure)
- [x] No cross-root runtime coupling introduced; integration only through versioned contracts
- [x] Contract impact classified (breaking/non-breaking) and versioning impact declared
- [x] Typed error mapping and stable error codes defined for new failure modes
- [x] Financial/time invariants respected (Decimal-only money, percentage 0–100, UTC aware datetime)
- [x] TDD strategy declared (red -> green -> refactor) for functional changes
- [x] Contract tests included when any contract surface changes
- [x] API responses exclude null-valued optional fields unless the endpoint contract explicitly requires their presence
- [x] Spec updates identified for behavior changes
- [x] ADR updates/new ADR identified for structural or architectural changes
- [x] CI quality gates impacted by this feature are listed (lint, type-check, tests, contracts)

Gate result (pre-Phase 0): PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-pagination-rules-sync/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
docs/
├── spec/
│   └── features/
│       ├── F-0001-acceso-y-autenticacion-operador.md
│       ├── F-0002-propietarios-sujetos-fiscales.md
│       └── F-0003-propiedades-y-titularidad.md
├── roadmap.md
└── dependency-graph.yaml

backend/
├── src/
└── tests/
  ├── contract/
  └── integration/

specs/001-pagination-rules-sync/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

**Structure Decision**: Multi-root existente sin cambios estructurales. El alcance de implementacion se concentra en documentacion funcional (`docs/spec/features`) y validacion de contratos/pruebas en `backend/tests` cuando exista superficie de colecciones.

## Dependency Graph Check

- Item de trabajo: sincronizacion de comportamiento en features existentes F-0001, F-0002 y F-0003.
- Dependencias satisfechas segun DAG:
  - F-0001 depende de EN-0100 (done)
  - F-0002 depende de F-0001 (done)
  - F-0003 depende de F-0002 (done)
  - EN-0202 (done, `affects_future_features: true`) aplica como baseline transversal.
- Orden de implementacion consistente: actualizar specs de F-0001 -> F-0002 -> F-0003 (o en paralelo) sin requerir items posteriores.
- No se detecta requerimiento de features/enablers futuros.

Dependency Graph Issue: none.

## ADR Alignment

- ADR-0004 (HTTP API y paginacion): la implementacion reforzara paginacion obligatoria en colecciones/listados/busquedas y evitara listas no acotadas.
- ADR-0006 (versionado y disciplina contractual): cualquier ajuste de superficie contractual se tratara como no-breaking dentro de MAJOR vigente; se verificara compatibilidad.
- ADR-0013 (configuration system): defaults/limites solo via configuracion central con precedencia global declarada.
- ADR-0009 (errores/observabilidad): se preserva modelo de errores tipificados y correlacion cuando aplique en endpoints de coleccion.

ADR Gap: none.

## Architectural Impact

- Contratos HTTP: ajuste/normalizacion de criterios para listados y busquedas en specs de F-0001/F-0002/F-0003.
- Eventos: sin cambios.
- Persistencia: sin cambios de esquema ni migraciones.
- Configuracion: se refuerza consumo exclusivo de EN-0202 para parametros de paginacion.
- Modelo de errores: sin nuevos tipos; mantener consistencia de mapeos existentes.

Versioning impact: non-breaking expected; no MAJOR bump planned.

## Constitution Consistency

- Dinero/porcentajes/UTC: sin cambios de semantica; se preservan invariantes existentes.
- Error model: se mantiene tipificado y estable.
- Dominio economico: no impactado.
- Idioma: documentacion funcional en espanol; codigo/logs tecnicos en ingles.

## Roadmap Consistency

- Alineado con roadmap: trabajo de coherencia sobre features `done` y baseline EN-0202.
- No introduce capacidades fuera de alcance.
- Respeta separacion Feature/Enabler: no redefine EN-0202, solo integra su regla en features existentes.

## Documentation Synchronization

- Actualizar/confirmar sincronia en:
  - `docs/spec/features/F-0001-acceso-y-autenticacion-operador.md`
  - `docs/spec/features/F-0002-propietarios-sujetos-fiscales.md`
  - `docs/spec/features/F-0003-propiedades-y-titularidad.md`
- Revisar si requiere nota de consistencia en `README.md` o `backend/README.md` (solo si se explicitan convenciones de listados).
- No se preven cambios de estado en `docs/roadmap.md` ni `docs/dependency-graph.yaml`.

## TDD and Quality Gates

- Estrategia TDD (cuando haya ajuste funcional):
  - red: pruebas de contrato/integracion que fallen ante ausencia de paginacion obligatoria o precedencia incorrecta.
  - green: ajuste de comportamiento/configuracion hasta pasar pruebas.
  - refactor: consolidar reglas sin hardcodes fuera de configuracion central.
- Quality gates impactados:
  - lint
  - type-check
  - unit tests (si hay validadores de parametros)
  - integration tests (colecciones)
  - contract tests (superficie HTTP de listados/busquedas)

## Phase Plan

### Phase 0 - Research

1. Validar politica de precedencia EN-0202 para todos los puntos de consumo de paginacion.
2. Confirmar comportamiento no-breaking de contratos de coleccion existentes.
3. Definir estrategia de prueba minima para cubrir F-0001/F-0002/F-0003.

Output: `research.md`

### Phase 1 - Design

1. Modelar artefactos funcionales afectados (regla transversal, parametros de lista, alcance por feature).
2. Definir contrato de comportamiento esperado para colecciones/listados/busquedas.
3. Elaborar quickstart de validacion para ejecucion local/CI.

Outputs:
- `data-model.md`
- `contracts/pagination-governance.md`
- `quickstart.md`

Post-design Constitution Check: PASS (sin violaciones).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| none | — | — |

## Implementation Traceability

### Files Created

| File | Purpose |
|------|---------|
| `backend/tests/contract/test_pagination_mandatory_collections.py` | Contract tests — mandatory pagination fields, bounded responses on all collection surfaces (US1, FR-001) |
| `backend/tests/integration/test_collection_responses_are_bounded.py` | Integration tests — response bounded by max_page_size config across F-0002/F-0003 surfaces (US1, FR-001/FR-002) |
| `backend/tests/contract/test_pagination_precedence_contract.py` | Contract tests — PAGINATION_MAX_PAGE_SIZE env var overrides built-in default on all surfaces (US2, FR-003/FR-004) |
| `backend/tests/integration/test_pagination_precedence_en0202.py` | Integration tests — full env > file > defaults precedence for both pagination keys (US2, SC-002) |
| `backend/tests/contract/test_no_hardcoded_pagination_defaults.py` | Regression tests — primary guard for FR-005; detects hardcoded default page_size in routers (US3) |
| `backend/tests/integration/test_pagination_limits_from_configuration.py` | Integration tests — max_page_size enforcement including edge values (FR-002/FR-003/FR-005, SC-004) |

### Files Modified — Source Code

| File | Change |
|------|--------|
| `backend/src/baku/backend/infrastructure/config/sources.py` | Added `PAGINATION_DEFAULT_PAGE_SIZE` and `PAGINATION_MAX_PAGE_SIZE` to `_ENV_VAR_TO_KEY` mapping |
| `backend/src/baku/backend/interfaces/http/api/v1/owners/router.py` | Added `_get_pagination_defaults()`; changed `page_size` to `int | None`; applied config-driven capping |
| `backend/src/baku/backend/infrastructure/persistence/sqlite/owners/repositories.py` | Removed `_MAX_PAGE_SIZE = 100` constant and secondary cap; capping is now exclusively at router level |
| `backend/src/baku/backend/interfaces/http/api/v1/properties/router.py` | Changed `page_size` to `int | None`; resolved default from `_get_pagination_defaults()` in both list endpoints |

### Files Modified — Specification Artifacts

| File | Change |
|------|--------|
| `docs/spec/features/F-0001-acceso-y-autenticacion-operador.md` | Added `environment variables > config file > defaults` precedence chain; explicit hardcode prohibition |
| `docs/spec/features/F-0002-propietarios-sujetos-fiscales.md` | Verified mandatory pagination and precedence chain (already compliant) |
| `docs/spec/features/F-0003-propiedades-y-titularidad.md` | Changed to "paginacion obligatoria"; added explicit precedence chain; hardcode prohibition |
| `specs/001-pagination-rules-sync/spec.md` | SC-001..SC-004 now reference coverage test files; US3 behavioral acceptance scenario added |
| `specs/001-pagination-rules-sync/research.md` | Added Collection Surface Matrix table and Hallazgos clave section |
| `specs/001-pagination-rules-sync/quickstart.md` | Added Section 3 with 4 EN-0202 precedence verification sub-steps |
| `specs/001-pagination-rules-sync/data-model.md` | Added Concrete Surface Bindings table and Transversal Enforcement Rule |
| `specs/001-pagination-rules-sync/contracts/pagination-governance.md` | Extended Rule 2 with config keys; added Rule 6 (cap at HTTP router layer) |

### ADR References

- ADR-0013: configuration system — `PAGINATION_DEFAULT_PAGE_SIZE` / `PAGINATION_MAX_PAGE_SIZE` now fully wired into `sources.py`
- ADR-0004: HTTP API pagination — behavior aligned across all collection surfaces
- ADR-0006: contract versioning — all changes classified non-breaking; no version bump required

### Test Coverage Summary

- 34 new tests across 6 files (279 total, 0 failures)
- Covers: US1 (mandatory pagination), US2 (EN-0202 precedence), US3 (no hardcoded defaults)
- Integration and contract layers both covered for F-0002 and F-0003 collection surfaces
