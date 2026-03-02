# Data Model — EN-0100 Project Bootstrap

## 1) RootIndependiente
- Description: Unidad autónoma dentro del monorepo para evolución y validación independiente.
- Fields:
  - `name` (enum): `backend` | `bot`
  - `namespace_prefix` (string): prefijo de namespace por root
  - `has_pyproject` (bool)
  - `has_src` (bool)
  - `has_tests` (bool)
- Validation rules:
  - `name` MUST ser único por root.
  - `has_pyproject`, `has_src` y `has_tests` MUST ser `true` para considerar bootstrap válido.

## 2) EstructuraMinimaRoot
- Description: Conjunto mínimo de artefactos por root para habilitar desarrollo reproducible.
- Fields:
  - `root_name` (ref -> RootIndependiente.name)
  - `artifacts` (set): `pyproject`, `src`, `tests`
  - `status` (enum): `missing` | `complete`
- Validation rules:
  - `status=complete` solo si todos los artefactos requeridos existen.

## 3) CIPipelinePR
- Description: Validación automática mínima ejecutada en PR.
- Fields:
  - `trigger` (enum): `pull_request`
  - `checks_per_root` (set): `lint`, `typing`, `smoke_tests`
  - `roots_covered` (set): `backend`, `bot`
  - `result` (enum): `pass` | `fail`
- Validation rules:
  - Debe incluir los tres checks por cada root cubierto.
  - Si falta un root o un check obligatorio, `result` MUST ser `fail`.

## 4) SmokeTestRoot
- Description: Test mínimo por root para validar ejecución del runner.
- Fields:
  - `root_name` (ref -> RootIndependiente.name)
  - `is_present` (bool)
  - `last_execution_status` (enum): `pass` | `fail` | `not_run`
- Validation rules:
  - `is_present` MUST ser `true` en roots iniciales.

## Relationships
- `RootIndependiente` 1..1 `EstructuraMinimaRoot`
- `RootIndependiente` 1..1 `SmokeTestRoot`
- `CIPipelinePR` N..N `RootIndependiente`

## State Transitions

### EstructuraMinimaRoot.status
- `missing` -> `complete` cuando existen artefactos mínimos requeridos.
- `complete` -> `missing` si se elimina artefacto obligatorio.

### CIPipelinePR.result
- `pass` -> `fail` ante incumplimiento de lint/tipado/smoke en cualquier root.
- `fail` -> `pass` tras corregir incumplimientos y re-ejecutar pipeline.
