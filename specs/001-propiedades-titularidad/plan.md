# Implementation Plan: F-0003 Propiedades y Titularidad

**Branch**: `001-propiedades-titularidad` | **Date**: 2026-03-10 | **Spec**: `specs/001-propiedades-titularidad/spec.md`
**Input**: Feature specification from `specs/001-propiedades-titularidad/spec.md`

## Summary

Implementar la gestion de propiedades y titularidad actual (sin historico) como master data auditable,
con soft-delete en cascada de titularidades, porcentajes en rango 0-100 (hasta 2 decimales) y contrato
HTTP aditivo en `/api/v1`, preservando arquitectura hexagonal, modelo de errores tipificados,
serializacion temporal UTC y omision de campos `null` en respuestas.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, SQLAlchemy, PyJWT, pytest, mypy, ruff  
**Storage**: SQLite con migraciones versionadas (Alembic)  
**Testing**: pytest (unit, integration, contract) con baseline de DB en memoria para integracion  
**Target Platform**: backend self-hosted en LAN, despliegue por contenedor Linux  
**Project Type**: Monorepo multi-root; implementacion funcional en `backend`  
**Performance Goals**: listados paginados de propiedades con p95 <= 250 ms para `page_size=50` en dataset local de referencia (hasta 10k propiedades)  
**Constraints**: UTC obligatorio; errores tipificados con `correlation_id`; sin PII en logs por defecto; sin imports runtime cruzados entre roots; sin campos `null` en respuesta publica  
**Scale/Scope**: MVP1, operador unico, sin eventos, sin operaciones economicas de ledger

## ADR Impact Matrix (Obligatorio)

### ADRs materialmente impactados

- **ADR-0001 (Monorepo multi-root)**: cambios solo en `backend`; integracion con otros roots via contrato versionado, sin runtime sharing.
- **ADR-0002 (Hexagonal Architecture)**: nuevo modulo de dominio para Property/Ownership, casos de uso en Application y adapters HTTP separados.
- **ADR-0003 (SQLite + SQLAlchemy + migrations)**: nuevas entidades de persistencia para propiedades y titularidades con transacciones explicitas y migraciones.
- **ADR-0004 (HTTP + OpenAPI + versioning)**: nueva superficie de recurso en `/api/v1/properties` y consultas asociadas, con paginacion.
- **ADR-0005 (JWT stateless)**: autenticacion obligatoria en toda operacion de la feature.
- **ADR-0006 (Contract versioning discipline)**: cambio aditivo no-breaking en MAJOR vigente.
- **ADR-0009 (Error model + observability)**: errores tipificados y logging estructurado con correlacion.
- **ADR-0011 (Monetary and percentage representation)**: `ownership_percentage` como Decimal 0-100 con precision maxima definida.
- **ADR-0012 (Time handling policy)**: timestamps UTC ISO-8601 con `Z`; fechas puras en `YYYY-MM-DD`.
- **ADR-0013 (Configuration system)**: parametros de paginacion (`page_size`, `max_page_size`) configurables de forma centralizada y validada.

### ADRs no impactados materialmente

- **ADR-0010**: no se introducen eventos ni publicacion asyncrona.
- **ADR-0014**: no se introducen operaciones economicas con efecto contable.

## Declaraciones obligatorias

- **Cambios de contrato (HTTP/eventos)**: SI (HTTP), NO (eventos).
- **Clasificacion de impacto de contrato**: no-breaking (aditivo en `v1`).
- **Cambios de persistencia (migraciones)**: SI (tablas/indices y restricciones para propiedades y titularidades).
- **Introduccion de eventos**: NO.
- **Implicaciones de versionado**: se mantiene MAJOR actual (`/api/v1`).
- **ADR Gap**: NO.

## Dependency Graph Check

- Dependencia declarada de F-0003: `F-0002` (estado `done`) satisfecha.
- Enablers previos aplicables (`affects_future_features: true`) ya integrados y asumidos: `EN-0100`, `EN-0202`, `EN-0200`, `EN-0201`, `EN-0300`.
- No se requieren items posteriores (`F-0004+`, `EN-0301`, `EN-0207`, `EN-0302`) para implementar este slice.

**Dependency Graph Issue**:

- La especificacion funcional fuente `docs/spec/features/F-0003-propiedades-y-titularidad.md` mantiene "(ninguna explicita)" en dependencias, mientras que el DAG oficial establece dependencia a `F-0002`. Para implementacion y planning se toma el DAG como fuente de verdad.

## Constitution Check (Pre-Research)

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

## Phase 0 - Research Output

Decisiones consolidadas en `research.md`:

1. Regla operativa de titularidad parcial (total permitido 100, suma <100 aceptada, >100 rechazada).
2. Precision y representacion de porcentaje (Decimal 0-100, maximo 2 decimales).
3. Invariante de unicidad activa por par (`property_id`, `owner_id`) con compatibilidad de soft-delete.
4. Politica de derivados catastrales (`cadastral_construction_value`, `construction_ratio`) y no editabilidad.
5. Contrato de paginacion y configurabilidad transversal (`page_size`, `max_page_size`).
6. Contrato temporal y de serializacion (`ISO-8601 UTC Z` y `YYYY-MM-DD`).
7. Politica de logs sin PII y error model tipificado con `correlation_id`.

## Phase 1 - Design Output

Artefactos generados:

- `data-model.md`: entidades Property, Ownership y referencias a Owner, con validaciones, estados y transiciones.
- `contracts/properties-api-v1.yaml`: contrato HTTP aditivo para CRUD de propiedades y gestion de titularidad.
- `contracts/error-model.md`: catalogo de errores tipificados especificos de la feature.
- `quickstart.md`: flujo de validacion manual y gates de calidad.

## Constitution Check (Post-Design Re-check)

- [x] Limites de capas preservados en el diseno.
- [x] Aislamiento multi-root preservado sin runtime sharing.
- [x] Impacto contractual HTTP clasificado como aditivo no-breaking.
- [x] Errores tipificados y mapeo consistente definidos.
- [x] Disciplina temporal UTC y formatos de fecha especificados.
- [x] Porcentajes 0-100 con precision explicita y sin representacion 0-1 en contrato.
- [x] Contract tests definidos para nueva superficie HTTP.
- [x] Cambios de comportamiento reflejados en spec y plan.
- [x] No se requiere ADR nuevo ni modificacion de ADR vigente.
- [x] Gates de CI impactados listados.

## Architectural Impact

- **HTTP contracts**: nueva superficie de recursos de propiedades/titularidad en `/api/v1`; cambio aditivo.
- **Events**: sin publicacion de eventos en este slice.
- **Persistence**: nuevas entidades de master data con auditoria y soft-delete; soft-delete en cascada de titularidades al eliminar propiedad.
- **Configuration**: se consumen parametros centralizados para paginacion (`page_size`, `max_page_size`) sin lecturas ad-hoc de entorno.
- **Error model**: extiende catalogo de errores tipificados existentes para validaciones de dominio de propiedad/titularidad.
- **Versioning impact**: no-breaking en MAJOR actual.

## Documentation and Roadmap Sync

Documentacion a actualizar/sincronizar durante implementacion:

- `docs/spec/features/F-0003-propiedades-y-titularidad.md` (alinear dependencias declaradas con DAG oficial y reglas cerradas de la feature).
- `backend/README.md` (nueva superficie HTTP y reglas de uso de propiedades/titularidad).
- `README.md` (estado de capacidades funcionales al completar feature).
- `docs/roadmap.md` (estado F-0003: `planned -> in_progress -> done`).
- `docs/dependency-graph.yaml` (sin cambios de aristas; sincronizar estado de F-0003).

## Project Structure

### Documentation (this feature)

```text
specs/001-propiedades-titularidad/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── properties-api-v1.yaml
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

**Structure Decision**: F-0003 se implementa en `backend`, reutilizando baseline de composicion HTTP (EN-0300), configuracion centralizada (EN-0202), observabilidad (EN-0200) y baseline de pruebas en DB en memoria (EN-0201). `bot` no recibe cambios funcionales en este slice.

## CI Quality Gates Impacted

- `ruff check` en `backend/src` y `backend/tests`
- `mypy` en `backend/src`
- `pytest` unit/integration/contract para propiedades y titularidad
- contract tests de endpoints de propiedades y titularidad, incluyendo autenticacion, paginacion, omision de `null`, validacion de porcentaje y soft-delete en cascada

## Complexity Tracking

Sin violaciones constitucionales justificadas.
