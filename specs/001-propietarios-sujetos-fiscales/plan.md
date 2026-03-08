# Implementation Plan: F-0002 Propietarios (Sujetos Fiscales)

**Branch**: `001-propietarios-sujetos-fiscales` | **Date**: 2026-03-08 | **Spec**: `specs/001-propietarios-sujetos-fiscales/spec.md`
**Input**: Feature specification from `specs/001-propietarios-sujetos-fiscales/spec.md`

## Summary

Implementar y mantener la gestion CRUD de propietarios como master data fiscal con soft delete auditable,
normalizacion de tax_id, autenticacion obligatoria, filtros y paginacion consistente, manteniendo
arquitectura hexagonal y contrato HTTP aditivo en `/api/v1`, incorporando el cambio de modelo de
`entity_type` y los nuevos campos de identidad/contacto (`first_name`, `last_name`,
`stamp_image`, `land_line`, `land_line_country_code`, `mobile`, `mobile_country_code`).

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, SQLAlchemy, PyJWT, pytest, mypy, ruff  
**Storage**: SQLite con migraciones versionadas  
**Testing**: pytest (unit, integration, contract) con DB en memoria para integracion  
**Target Platform**: backend self-hosted en LAN (contenedores Linux)  
**Project Type**: Monorepo multi-root, implementacion funcional en root `backend`  
**Performance Goals**: para `GET /api/v1/owners`, p95 <= 250 ms con `page_size=50` sobre dataset de 10,000 owners en entorno local de referencia (LAN/self-hosted), manteniendo metadatos de paginacion correctos y orden estable  
**Constraints**: UTC obligatorio, errores tipificados, sin PII en logs, sin imports runtime cruzados entre roots, campos `null` omitidos en respuestas publicas  
**Scale/Scope**: MVP1, operador unico, sin relaciones owner-propiedad aun, sin eventos

## ADR Impact Matrix (Obligatorio)

### ADRs materialmente impactados

- **ADR-0002 (Hexagonal Architecture)**: modulo de dominio para Owner y casos de uso en Application, con adapters HTTP e infraestructura separados.
- **ADR-0003 (SQLite + SQLAlchemy + migrations)**: persistencia `owners` con transacciones explicitas y migracion versionada.
- **ADR-0004 (HTTP + OpenAPI + versioning)**: superficie de recurso `/api/v1/owners` y contrato paginado.
- **ADR-0005 (JWT stateless)**: todos los endpoints de owners requieren autenticacion vigente.
- **ADR-0006 (Contract versioning discipline)**: cambio aditivo no-breaking de contrato HTTP en MAJOR actual.
- **ADR-0009 (Error model + observability)**: errores tipificados con `error_code` estable y `correlation_id`; logs estructurados sin PII.
- **ADR-0012 (UTC policy)**: `created_at`, `updated_at`, `deleted_at` siempre UTC.

### ADRs no impactados materialmente

- **ADR-0010**: no se introducen eventos.
- **ADR-0011**: no hay dinero ni porcentajes en esta feature.
- **ADR-0013/0014**: sin nuevas reglas de configuracion global ni idempotencia economica.

## Declaraciones obligatorias

- **Cambios de contrato (HTTP/eventos)**: SI (HTTP), NO (eventos).
- **Clasificacion de impacto de contrato**: no-breaking (aditivo en `v1`).
- **Cambios de persistencia (migraciones)**: SI (nueva tabla/indices para owners y evolucion de esquema por nuevos campos).
- **Introduccion de eventos**: NO.
- **Implicaciones de versionado**: se mantiene MAJOR actual (`/api/v1`).
- **ADR Gap**: NO.

## Dependency Graph Check

- Dependencia declarada de F-0002: `F-0001` (estado `done`) satisfecha.
- Enablers previos aplicables (`affects_future_features: true`) disponibles y asumidos: `EN-0100`, `EN-0202`, `EN-0200`, `EN-0201`, `EN-0300`.
- No se requieren features/enablers posteriores (`F-0003+`, `EN-0207`, `EN-0301`, etc.) para implementar F-0002.

**Dependency Graph Issue**: None.

## Constitution Check (Pre-Research)

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

## Phase 0 - Research Output

Decisiones consolidadas en `research.md`:

1. Estrategia de normalizacion de tax_id para unicidad y busqueda.
2. Politica de auditoria obligatoria (`created_by`, `updated_by`, `deleted_by`) alineada con constitucion.
3. Contrato de `include_deleted` consistente para detalle y listado.
4. Regla de observabilidad sin PII en logs de propietarios.
5. Compatibilidad de paginacion/filtros dentro de `v1` sin romper contratos existentes.
6. Evolucion del modelo de identidad/contacto: `entity_type` y campos extendidos (`first_name`, `last_name`, `stamp_image`, `land_line`, `mobile`, codigos de pais) manteniendo compatibilidad aditiva en v1.

## Phase 1 - Design Output

Artefactos generados/actualizados:

- `data-model.md`: entidad Owner, validaciones, estados y reglas de transicion con nuevos campos de identidad/contacto.
- `contracts/owners-api-v1.yaml`: contrato HTTP para CRUD, listado y busqueda con `entity_type` y contacto extendido.
- `contracts/error-model.md`: catalogo de errores tipificados para owners.
- `quickstart.md`: flujo de validacion local y gates de calidad.

## Constitution Check (Post-Design Re-check)

- [x] Limites de capas preservados en el diseno.
- [x] Aislamiento multi-root preservado sin runtime sharing.
- [x] Impacto contractual HTTP clasificado como aditivo no-breaking.
- [x] Errores tipificados y mapeo consistente definidos.
- [x] Disciplina temporal UTC aplicada a campos de auditoria.
- [x] Contract tests definidos para nueva superficie HTTP.
- [x] Cambios de comportamiento reflejados en spec y plan (incluyendo renombres y nuevos campos).
- [x] No se requiere ADR nuevo o modificacion de ADR vigente.
- [x] Gates de CI impactados listados.

## Architectural Impact

- **HTTP contracts**: recurso `/api/v1/owners` con operaciones POST/GET(list)/GET(detail)/PATCH/DELETE; payloads alineados con `entity_type` y contacto extendido.
- **Eventos**: sin cambios, no se introducen eventos.
- **Persistencia**: agregado Owner en SQLite con soft delete auditable y evolucion de columnas para los nuevos campos.
- **Configuracion**: sin nuevas claves obligatorias.
- **Modelo de errores**: variantes funcionales dentro del modelo tipificado existente.
- **Versionado**: cambio aditivo en v1, sin incremento de MAJOR.

## Documentation and Roadmap Sync

Documentacion a mantener sincronizada durante implementacion:

- `backend/README.md` (endpoints y comportamiento de filtros/soft delete y campos actuales).
- `docs/spec/roadmap.md` (estado F-0002: `planned -> in_progress -> done`).
- `docs/spec/dependency-graph.yaml` (estado F-0002 sincronizado con roadmap).
- `docs/spec/features/F-0002-propietarios-sujetos-fiscales.md` (alineado con cambios de campos).

## Project Structure

### Documentation (this feature)

```text
specs/001-propietarios-sujetos-fiscales/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── owners-api-v1.yaml
│   └── error-model.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/baku/backend/
│   ├── domain/
│   ├── application/
│   ├── interfaces/http/
│   └── infrastructure/
└── tests/
    ├── contract/
    └── integration/

bot/
├── src/baku/bot/
└── tests/
```

**Structure Decision**: F-0002 se implementa solo en `backend`, reutilizando el baseline de bootstrap HTTP (EN-0300), configuracion (EN-0202), logging (EN-0200) y tests in-memory (EN-0201). El root `bot` no recibe cambios funcionales en esta feature.

## CI Quality Gates Impacted

- `ruff check` en `backend/src` y `backend/tests`
- `mypy` en `backend/src`
- `pytest` unit/integration/contract para owners
- contract tests de `/api/v1/owners` con validacion de `entity_type`, campos de contacto extendidos y omision de campos `null` en respuestas

## Complexity Tracking

Sin violaciones constitucionales justificadas.
