# Quickstart: EN-0300 Implementation Validation

**Status**: Implementado. Última actualización: 2026-03-07.

## Goal
Validar que EN-0300 reorganiza el bootstrap HTTP del `backend` con responsabilidades separadas, composition root único y fail-fast en errores críticos, sin cambios contractuales externos.

## 1. Preparar entorno
```bash
cd backend/
pip install -e ".[dev]"
```

## 2. Validar límites del entrypoint HTTP

```bash
pytest tests/integration/bootstrap/test_entrypoint_boundaries.py -v
```

Verificaciones clave:
- `main.py` expone `app` a través de `create_app()` (no construye `FastAPI()` directamente).
- `main.py` no contiene imports de `infrastructure/`, `add_middleware`, `include_router`, ni `dependency_overrides`.

## 3. Validar separación de responsabilidades de bootstrap

```bash
pytest tests/integration/bootstrap/test_bootstrap_responsibility_separation.py -v
```

Verifica que cada responsabilidad del inventario cerrado tiene su módulo dedicado:

| Responsabilidad | Módulo |
|---|---|
| `APP_CREATION` | `interfaces/http/bootstrap/app_factory.py` |
| `LIFESPAN_BOOTSTRAP` | `interfaces/http/bootstrap/lifespan.py` |
| `DEPENDENCY_COMPOSITION_WIRING` | `interfaces/http/bootstrap/dependency_wiring.py` |
| `MIDDLEWARE_REGISTRATION` | `interfaces/http/bootstrap/middleware_registry.py` |
| `ERROR_HANDLERS_REGISTRATION` | `interfaces/http/bootstrap/error_handlers_registry.py` |
| `ROUTER_REGISTRATION` | `interfaces/http/bootstrap/router_registry.py` |

## 4. Validar composition root único

```bash
pytest tests/integration/bootstrap/test_single_composition_root.py tests/integration/bootstrap/test_dependency_wiring_equivalence.py -v
```

Verifica:
- Solo `dependency_wiring.py` importa desde `infrastructure/` en el paquete bootstrap.
- `wire_dependencies()` produce exactamente el mismo conjunto de overrides que el `main.py` original.
- La llamada es idempotente.

## 5. Validar fail-fast de bootstrap y trazabilidad de error

```bash
pytest tests/integration/bootstrap/test_fail_fast_bootstrap_errors.py tests/integration/bootstrap/test_bootstrap_error_traceability.py -v
```

Verifica:
- `lifespan.py` invoca `RuntimeConfigurationProvider().get_profile()` — punto de entrada fail-fast (ADR-0013).
- `AggregatedConfigurationError` se levanta cuando se ausenta un secreto requerido.
- Respuestas de error incluyen `correlation_id`, `error_code`, `message` (ADR-0009, constitución §III).

## 6. Validar no impacto contractual (superficie HTTP invariante)

```bash
pytest tests/integration/bootstrap/test_http_surface_unchanged.py -v
```

Verifica que el conjunto de rutas y métodos HTTP es exactamente el mismo que antes de EN-0300:
- `POST /api/v1/auth/bootstrap`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `PUT /api/v1/auth/password`

## 7. Quality gates mínimos

```bash
# Lint
python -m ruff check src/ tests/

# Type check
python -m mypy src/

# Regresión completa (incluye bootstrap + contrato)
pytest tests/

# Todo junto
python -m ruff check src/ tests/ && python -m mypy src/ && pytest tests/
```
