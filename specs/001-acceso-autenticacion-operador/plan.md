# Implementation Plan: F-0001 Acceso y Autenticación (Operador)

**Branch**: `001-acceso-autenticacion-operador` | **Date**: 2026-03-03 | **Spec**: `specs/001-acceso-autenticacion-operador/spec.md`
**Input**: Feature specification from `/specs/001-acceso-autenticacion-operador/spec.md`

## Summary

Definir e implementar la capacidad de autenticación del operador único para MVP1,
incluyendo bootstrap inicial, login, logout con revocación explícita del token actual,
rotación de contraseña con revocación global por versión de credencial, TTL configurable,
bloqueo temporal por intentos fallidos (base 5/15 configurable) y auditoría mínima de acceso.

## Technical Context

**Language/Version**: Python 3.11 (roots `backend` y `bot`)  
**Primary Dependencies**: FastAPI (adapter HTTP), JWT stateless, pytest, mypy, ruff  
**Storage**: SQLite (estado de operador, versión de credencial, revocación por token actual, auditoría, bloqueo temporal)  
**Testing**: pytest (unitarias, integración SQLite y contract tests para API de autenticación)  
**Target Platform**: Servicio self-hosted en LAN, Linux containers
**Project Type**: Monorepo multi-root de servicios backend + bot  
**Performance Goals**: login válido p95 < 2s en operación local; revocación efectiva inmediata tras cambio de contraseña  
**Constraints**: operador único, UTC obligatorio, errores tipificados, sin cross-root imports, sin sesiones server-side globales  
**Scale/Scope**: alcance F-0001 para MVP1, sin RBAC/SSO/multiusuario

## ADR Impact Matrix (Obligatorio)

### ADRs materialmente impactados

- **ADR-0003 (Persistence SQLite + transactions)**: F-0001 introduce persistencia de estado de autenticación, bloqueo temporal y auditoría con operaciones state-changing transaccionales.
- **ADR-0004 (HTTP API + versioning)**: se introducen endpoints de bootstrap/login/logout/rotación con contrato versionado y errores tipificados.
- **ADR-0005 (JWT stateless + revocación por ver)**: se aplica emisión JWT con `ver`, validación stateless y revocación global tras cambio de contraseña; adicionalmente logout revoca token actual.
- **ADR-0006 (Contract versioning + integration)**: hay cambio de superficie contractual HTTP; requiere actualización y validación por contract tests.
- **ADR-0008 (CI governance)**: feature impacta gates de lint, type-check, unit/integration y contract tests en PR.
- **ADR-0009 (Error model + observability)**: autenticación debe mapear errores tipificados, código estable, mensaje en español y `correlation_id`.
- **ADR-0012 (UTC policy)**: `iat`, `exp`, `last_login_at`, `created_at`, `updated_at` y bloqueo temporal en UTC.

### ADRs no impactados materialmente

- **ADR-0001**: sin cambios estructurales de roots (se mantiene aislamiento).
- **ADR-0002**: sin cambios de principio; solo aplicación de separación por capas.
- **ADR-0007**: sin cambios de modelo de entrega.
- **ADR-0010**: no se introducen eventos.
- **ADR-0011**: sin lógica monetaria/porcentajes.

## Declaraciones obligatorias

- **Cambios de contrato (HTTP/eventos)**: **SÍ** (HTTP), **NO** (eventos).
- **Clasificación de impacto de contrato**: **no-breaking** dentro de MAJOR actual (superficie aditiva).
- **Cambios de persistencia (migraciones)**: **SÍ** (nuevas estructuras para autenticación).
- **Introducción de eventos**: **NO**.
- **Implicaciones de versionado**: mantener MAJOR actual; garantizar retrocompatibilidad y errores estables.
- **ADR Gap**: **NO** (cobertura completa por ADR-0003/4/5/6/8/9/12).

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

Research tasks resolved en `research.md`:

1. Patrón de revocación de token actual en logout compatible con JWT stateless.
2. Política de bloqueo temporal configurable (base 5/15) y consideraciones de seguridad.
3. Modelado de auditoría mínima obligatoria (`created_at`, `last_login_at`, `updated_at` nullable).
4. Estrategia de contract testing para nuevas rutas de autenticación sin romper MAJOR.

## Phase 1 — Design Output

Artifacts de diseño:

- `data-model.md`: entidades y relaciones para operador, credencial, token revocado y bloqueo temporal.
- `contracts/`: contrato HTTP de autenticación (v1) y esquema de errores tipificados.
- `quickstart.md`: flujo de validación manual/local (bootstrap→login→logout→rotación→bloqueo).

## Constitution Check (Post-Design Re-check)

- [x] Límite de capas preservado en diseño.
- [x] Aislamiento multi-root preservado sin runtime sharing.
- [x] Impacto contractual HTTP clasificado como aditivo no-breaking.
- [x] Errores tipificados y mapeo consistente definidos.
- [x] Tiempo en UTC aplicado a tokens, auditoría y bloqueo.
- [x] Contract tests incluidos para superficie HTTP nueva.
- [x] Spec y trazabilidad SDD actualizadas en el mismo change set.
- [x] No se requiere ADR nuevo o modificación de ADR vigente.
- [x] Gates de CI impactados listados (lint, mypy, unit, integration, contracts).

## Project Structure

### Documentation (this feature)

```text
specs/001-acceso-autenticacion-operador/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── auth-api-v1.yaml
│   └── error-model.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/baku/backend/
└── tests/

bot/
├── src/baku/bot/
└── tests/

specs/
└── 001-acceso-autenticacion-operador/
```

**Structure Decision**: la implementación se concentra en `backend` para la superficie HTTP de autenticación; `bot` permanece sin cambios funcionales directos en F-0001, respetando ADR-0001.

## Complexity Tracking

Sin violaciones constitucionales justificadas.
