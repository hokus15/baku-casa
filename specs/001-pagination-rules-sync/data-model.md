# Data Model - Pagination Rules Sync

## Scope

This item does not introduce new domain entities. It defines and synchronizes behavior-level governance objects used by existing collection/list/search flows.

## Entity: PaginationPolicy

- Description: Transversal policy applied to collection endpoints in F-0001/F-0002/F-0003.
- Fields:
  - `pagination_required` (boolean, always true for applicable collections)
  - `default_page` (integer, from centralized configuration)
  - `default_page_size` (integer, from centralized configuration)
  - `max_page_size` (integer, from centralized configuration)
  - `precedence` (fixed enum: env_over_file_over_defaults)
- Validation rules:
  - Pagination must always be enabled for collection/list/search surfaces.
  - `default_page_size` must be positive.
  - `max_page_size` must be >= `default_page_size`.
- Relationships:
  - Applied to feature specs F-0001, F-0002, and F-0003 where collection endpoints exist.

## Entity: PaginationConfigurationSource

- Description: Logical source resolution model from EN-0202.
- Values (ordered):
  1. environment variables
  2. config file
  3. defaults
- Validation rules:
  - Resolution order is deterministic and immutable at specification level.
  - No alternative precedence is allowed.

## Entity: CollectionSurface

- Description: Any list/search API surface returning a bounded subset of resources.
- Fields:
  - `feature_id` (F-0001 | F-0002 | F-0003)
  - `surface_type` (list | search)
  - `requires_pagination_policy` (boolean)
- State transitions:
  - `unspecified` -> `aligned`
  - `aligned` -> `regressed` (only via unauthorized spec/code drift; must fail quality checks)

## Concrete Surface Bindings (from research.md matrix)

| Feature | Endpoint | `requires_pagination_policy` | Notes |
|---------|----------|------------------------------|-------|
| F-0001 | (ninguno activo) | false (preventivo) | Declaracion documental preventiva |
| F-0002 | `GET /api/v1/owners` | true | Lista + busqueda; requiere alineacion completa |
| F-0003 | `GET /api/v1/properties` | true | Listado; requiere alineacion completa |
| F-0003 | `GET /api/v1/owners/{owner_id}/properties` | true | Listado cruzado; requiere alineacion completa |

## Transversal Enforcement Rule

La `PaginationPolicy` con `pagination_required=true` DEBE aplicarse a todas las superficies con `requires_pagination_policy=true`. La implementacion conforme debe:

1. NO declarar `default_page_size` ni `max_page_size` como constantes en routers, servicios de aplicacion ni repositorios.
2. Resolver `default_page_size` y `max_page_size` en tiempo de request desde `RuntimeConfigurationProvider` (ADR-0013).
3. Capear `page_size` al `max_page_size` configurado ANTES de pasar el valor a la capa de aplicacion.
4. Usar `default_page_size` cuando el cliente no proporcione `page_size` explicitamente.

## Non-Goals

- No new persistence models.
- No migration requirements.
- No changes to monetary or temporal domain models.
