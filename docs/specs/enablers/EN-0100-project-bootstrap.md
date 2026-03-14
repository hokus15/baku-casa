# EN-0100: Project Bootstrap

## Objetivo
Establecer la base mínima del repositorio para habilitar el desarrollo reproducible mediante Spec Driven Development (SDD), antes de implementar cualquier funcionalidad de dominio.

## Descripción
Este enabler define la estructura inicial del monorepo multi-root y garantiza que existe un pipeline de CI funcional con tests mínimos por root.

## Incluye
- Estructura monorepo multi-root con roots independientes:
  - `backend/`
  - `bot/`
  - (posibilidad de añadir nuevos roots en el futuro)
- Estructura mínima por root:
  - `pyproject.toml`
  - `src/`
  - `tests/`
- Directorios de documentación base:
  - `docs/spec/`
  - `docs/adr/`
- `README.md` en la raíz con descripción funcional del proyecto y cómo ejecutar validaciones básicas.
- Workflow de CI (GitHub Actions) que ejecute validaciones por root.
- Un test “smoke” mínimo por root para validar ejecución del runner de tests.

## Fuera de alcance
- Cualquier caso de uso o lógica de negocio.
- Endpoints reales.
- Persistencia, migraciones, modelos ORM.
- Automatizaciones avanzadas de CI (salvo lo mínimo necesario).

## Criterios de aceptación
- Existe la estructura multi-root con `backend/` y `bot/` y su estructura mínima (`pyproject.toml`, `src/`, `tests/`).
- Existe un `README.md` en la raíz.
- Existen `docs/spec/` y `docs/adr/`.
- Existe un workflow de CI que ejecuta tests de `backend` y `bot` en PR.
- El mínimo obligatorio de CI en cada PR es ejecutar smoke tests por cada root del monorepo.
- Existen tests mínimos en `backend/` y `bot/` que pasan en CI.
- No se han implementado funcionalidades de dominio ni endpoints como parte de este enabler.