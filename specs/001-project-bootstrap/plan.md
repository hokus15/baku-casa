# Implementation Plan: EN-0100 Project Bootstrap

**Branch**: `001-project-bootstrap` | **Date**: 2026-03-02 | **Spec**: `specs/001-project-bootstrap/spec.md`
**Input**: Feature specification from `/specs/001-project-bootstrap/spec.md`

## Summary

Implementar el bootstrap mínimo del monorepo multi-root para habilitar SDD reproducible:
estructura base de `backend` y `bot` con artefactos mínimos por root, documentación base,
y CI mínima por PR con `lint + tipado + smoke tests` por root. Alcance estrictamente
habilitador: sin lógica de dominio, sin endpoints reales y sin persistencia funcional.

## Technical Context

**Language/Version**: Python 3.x por root (versionado exacto definido en cada `pyproject.toml`)  
**Primary Dependencies**: Tooling de lint, tipado y pruebas por root; GitHub Actions para CI  
**Storage**: N/A para EN-0100 (sin modelo persistente funcional)  
**Testing**: Smoke tests por root + ejecución en CI por PR  
**Target Platform**: Entorno self-hosted en LAN y runners CI Linux
**Project Type**: Enabler de monorepo multi-root  
**Performance Goals**: Validación determinista del bootstrap en cada PR  
**Constraints**: Sin casos de uso de dominio, sin endpoints reales, sin migraciones, sin eventos  
**Scale/Scope**: 2 roots iniciales (`backend`, `bot`) con posibilidad de expansión futura

## ADR Impact Matrix (Obligatorio)

### ADRs materialmente impactados

- **ADR-0001 (Monorepo Multi-root)**: Se implementa aislamiento de roots, artefactos mínimos por root y disciplina de integración sin imports runtime cruzados.
- **ADR-0002 (Hexagonal)**: Se preserva separación de capas desde bootstrap; no se introduce lógica de negocio en adapters.
- **ADR-0006 (Contratos e Integración)**: Se declara explícitamente ausencia de cambios de contrato funcional en EN-0100 y se mantiene disciplina de versionado/contract testing para cambios futuros.
- **ADR-0007 (Delivery Model)**: El bootstrap mantiene alineación con modelo self-hosted y prepara base para despliegue reproducible sin exigir profile `events`.
- **ADR-0008 (CI y Governance)**: Se implementa CI mínima por PR (`lint + tipado + smoke` por root) como primer gate obligatorio del enabler.

### ADRs no impactados materialmente (sin cambio en este enabler)

- **ADR-0003**: Sin persistencia funcional ni migraciones.
- **ADR-0004**: Sin endpoints HTTP ni contrato OpenAPI nuevo/modificado.
- **ADR-0005**: Sin autenticación/JWT en este alcance.
- **ADR-0009**: Sin nuevas superficies de error funcional; observabilidad profunda fuera de alcance.
- **ADR-0010**: Sin publicación de eventos (no aplica outbox en EN-0100).
- **ADR-0011**: Sin lógica monetaria/porcentajes en este enabler.
- **ADR-0012**: Sin lógica temporal funcional en este enabler.

## Declaraciones obligatorias del Enabler

- **Cambios de contrato (HTTP/eventos)**: **NO**.
- **Cambios de persistencia (migraciones)**: **NO**.
- **Introducción de eventos**: **NO**.
- **Requiere profile `events` en docker-compose**: **NO**.
- **Implicaciones de versionado**: sin incremento de versión de contratos funcionales; se mantiene continuidad de baseline arquitectónica.
- **ADR Gap**: **NO** (no se requiere crear/modificar ADR para este alcance).

## Constitution Check (Pre-Research)

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Layer boundaries preserved (Domain/Application/Interfaces/Infrastructure)
- [x] No cross-root runtime coupling introduced; integration only through versioned contracts
- [x] Contract impact classified (breaking/non-breaking) and versioning impact declared
- [x] Typed error mapping and stable error codes defined for new failure modes
- [x] Financial/time invariants respected (Decimal-only money, percentage 0–100, UTC aware datetime)
- [x] Contract tests included when any contract surface changes
- [x] Spec updates identified for behavior changes
- [x] ADR updates/new ADR identified for structural or architectural changes
- [x] CI quality gates impacted by this feature are listed (lint, type-check, tests, contracts)

## Phase 0 — Research Output

Research tasks resolved in `research.md`:

1. Definir alcance exacto de CI mínima para EN-0100.
2. Definir frontera de “sin funcionalidad de dominio” para evitar scope creep.
3. Definir estrategia de cumplimiento ADR en bootstrap sin introducir contratos/persistencia/eventos.

## Phase 1 — Design Output

Design artifacts:

- `data-model.md`: entidades estructurales del enabler (Root, Estructura Mínima, Pipeline PR, Smoke Test).
- `contracts/`: declaración de no cambios de contrato funcional.
- `quickstart.md`: validación operativa mínima del bootstrap.

## Constitution Check (Post-Design Re-check)

- [x] Límite de capas preservado en diseño.
- [x] Aislamiento multi-root preservado sin runtime sharing.
- [x] Sin cambios de contrato; versionado sin impacto funcional.
- [x] Sin cambios de persistencia/migraciones.
- [x] Sin eventos ni outbox requeridos.
- [x] CI mínima definida y verificable por PR.
- [x] Documentación y trazabilidad SDD cubiertas.

## Project Structure

### Documentation (this feature)

```text
specs/001-project-bootstrap/
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
├── pyproject.toml
├── src/
└── tests/

bot/
├── pyproject.toml
├── src/
└── tests/

docs/
├── spec/
└── adr/

.github/
└── workflows/
```

**Structure Decision**: Se adopta estructura monorepo multi-root mínima con validación CI por root y sin incorporar runtime compartido.

## Implementation Strategy (alto nivel)

1. Crear/validar estructura mínima de roots (`backend`, `bot`) y documentación base.
2. Configurar pipeline PR con gates mínimos acordados (`lint + tipado + smoke` por root).
3. Añadir smoke tests mínimos por root y verificación CI en verde.
4. Verificar exclusiones del enabler (sin dominio/endpoints/persistencia/eventos).
5. Preparar siguiente fase (`/speckit.tasks`) sin abrir ADR Gap.

## Complexity Tracking

Sin violaciones constitucionales justificadas en este enabler.
