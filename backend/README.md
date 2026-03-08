# Backend Root

Root independiente del backend para bootstrap EN-0100.

## Feature F-0002: Propietarios (Sujetos Fiscales)

**Estado**: ✅ Implementado

CRUD de propietarios con arquitectura hexagonal:

- Crear propietario (`POST /api/v1/owners`) — 201 Created
- Listar propietarios con paginación y filtros (`GET /api/v1/owners`) — 200 OK
  - Query params: `page` (1-based), `page_size` (1–100), `legal_name` (parcial, case-insensitive), `tax_id` (exact normalized), `include_deleted` (default: false)
- Obtener propietario por ID (`GET /api/v1/owners/{owner_id}`) — 200 OK
  - Query param: `include_deleted=true` para incluir eliminados
- Actualizar propietario (`PATCH /api/v1/owners/{owner_id}`) — 200 OK (solo campos enviados)
- Eliminar propietario (soft-delete) (`DELETE /api/v1/owners/{owner_id}`) — 204 No Content
  - Idempotent: re-llamar sobre propietario ya eliminado devuelve 204

Todos los endpoints requieren autenticación JWT (`Authorization: Bearer <token>`).

El `tax_id` se normaliza de forma determinista: trim → mayúsculas → sin espacios → sin guiones.

**Evidencia de calidad (F-0002)**:

```
ruff check src/ tests/  →  All checks passed!
mypy src/               →  Success: no issues found in 93 source files
pytest -q               →  174 passed, 3 warnings in 77.90s
```

## Enabler E-0100: Project Bootstrap

Establecer la base mínima del repositorio para habilitar el desarrollo reproducible mediante Spec Driven Development (SDD), antes de implementar cualquier funcionalidad de dominio.

- Solo estructura mínima (`pyproject`, `src`, `tests`).
- Sin endpoints reales.
- Sin lógica de dominio.
- Con migraciones versionadas para esquema de datos (ADR-0003).

## Feature F-0001: Acceso y Autenticación (Operador)

Implementación del sistema de autenticación con arquitectura hexagonal (ADR-0002):

- Bootstrap de operador único (`POST /api/v1/auth/bootstrap`)
- Login con JWT stateless (`POST /api/v1/auth/login`)
- Logout con revocación por `jti` (`POST /api/v1/auth/logout`)
- Rotación de contraseña con revocación global por `credential_version` (`PUT /api/v1/auth/password`)
- Throttle configurable por intentos fallidos
- Middleware de `X-Correlation-ID` en todos los requests

## Enabler EN-0300: HTTP Bootstrap Modularization

**Estado**: ✅ Implementado (2026-03-07)

Reorganización estructural del bootstrap HTTP (`interfaces/http/bootstrap/`). El `main.py`
es ahora un thin entrypoint; todas las responsabilidades de arranque están separadas en
componentes con responsabilidad única:

| Responsabilidad | Módulo |
|---|---|
| App Creation | `interfaces/http/bootstrap/app_factory.py` |
| Lifespan Bootstrap | `interfaces/http/bootstrap/lifespan.py` |
| Dependency Composition Wiring | `interfaces/http/bootstrap/dependency_wiring.py` |
| Middleware Registration | `interfaces/http/bootstrap/middleware_registry.py` |
| Error Handlers Registration | `interfaces/http/bootstrap/error_handlers_registry.py` |
| Router Registration | `interfaces/http/bootstrap/router_registry.py` |

El composition root único (`dependency_wiring.py`) es el único módulo del paquete
`interfaces/` con permiso de importar desde `infrastructure/` (ADR-0002).

El comportamiento fail-fast ante configuración crítica ausente se mantiene intacto (ADR-0013).

**Cobertura de tests**: 37 tests de integración en `tests/integration/bootstrap/` validan:
- Límites del entrypoint (`test_entrypoint_boundaries.py`)
- Separación de responsabilidades del inventario cerrado (`test_bootstrap_responsibility_separation.py`)
- Composition root único y equivalencia de overrides (`test_single_composition_root.py`, `test_dependency_wiring_equivalence.py`)
- Fail-fast y comportamiento del lifespan (`test_fail_fast_bootstrap_errors.py`)
- Superficie HTTP invariante (`test_http_surface_unchanged.py`)
- Trazabilidad de errores estructurados (`test_bootstrap_error_traceability.py`)

## Gates de calidad locales

Ejecutar desde el directorio `backend/`:

```bash
# Lint (ruff)
python -m ruff check src/ tests/

# Type check (mypy — configurado en pyproject.toml)
python -m mypy src/

# Tests
pytest tests/

# Todo junto
python -m ruff check src/ tests/ && python -m mypy src/ && pytest tests/
```

### Instalación del entorno de desarrollo

```bash
pip install -e ".[dev]"
```

## Migraciones (Alembic)

La aplicación no crea/actualiza esquema en runtime. El esquema se gestiona
exclusivamente por migraciones versionadas.

Ejecutar desde `backend/`:

```bash
# Aplicar todas las migraciones
python -m alembic -c alembic.ini upgrade head

# Ver historial
python -m alembic -c alembic.ini history

# Ver revisión actual
python -m alembic -c alembic.ini current
```

### Dependencias de producción

| Paquete | Propósito |
|---|---|
| `fastapi` | HTTP adapter (ADR-0004) |
| `uvicorn[standard]` | ASGI server |
| `PyJWT` | Tokens JWT stateless (ADR-0005) |
| `bcrypt` | Hash de contraseñas (sin passlib) |
| `SQLAlchemy` | ORM + SQLite (ADR-0003) |
| `python-dotenv` | Carga de fichero `.env` para desarrollo local |

## Enabler EN-0202: Configuration System

Sistema centralizado y tipado para gestionar configuración de la aplicación (ADR-0013).

Toda la lectura de variables de entorno está centralizada en `infrastructure/config/sources.py`.
Ningún otro módulo accede directamente a `os.getenv`.

### Variables de entorno requeridas

| Variable | Requerida | Default | Descripción |
|---|---|---|---|
| `AUTH_JWT_SECRET` | **SÍ** | — | Secreto de firma JWT. Sin valor por defecto; la aplicación falla en el arranque si no está definida. |
| `AUTH_JWT_ALGORITHM` | NO | `HS256` | Algoritmo de firma JWT. |
| `AUTH_TOKEN_TTL_SECONDS` | NO | `3600` | TTL del token de acceso en segundos. |
| `AUTH_MAX_FAILED_ATTEMPTS` | NO | `5` | Máximo de intentos de login fallidos antes del lockout. |
| `AUTH_LOCKOUT_MINUTES` | NO | `15` | Duración del lockout en minutos. |
| `TEST_DATABASE_URL` | NO (solo tests) | — | Override explícito para persistencia en tests; tiene prioridad sobre `DATABASE_URL` en suites de testing. |

### Comportamiento de arranque

1. La aplicación valida la configuración **antes** de incluir ningún router.
2. Si alguna clave requerida está ausente, la aplicación aborta con el conjunto completo de errores de validación (fail-fast, ADR-0013).
3. Las claves no declaradas emiten un `WARNING` estructurado pero no bloquean el arranque.

### Precedencia de fuentes

```
environment variables > config file (.env) > built-in defaults
```

Para desarrollo local, crea un fichero `.env` en el raíz de `backend/` con las variables necesarias (ver `.env.example`).

## Enabler EN-0200: Application Logging Baseline

El backend carga perfiles de logging por entorno desde la raíz de `backend/`:

- `logging.dev.ini`
- `logging.test.ini`
- `logging.prod.ini`

Baseline operativo:

- Doble salida de fichero: JSON + human-friendly.
- Campos mínimos por evento: `timestamp`, `level`, `service_name`, `correlation_id`, `message`.
- Correlación por request con `X-Correlation-ID` (propagado o generado).
- Rotación diaria a las 00:00 Europe/Madrid.
- Retención inicial de 7 días para logs rotados (configurable por entorno).

Fallback seguro:

- Si el perfil activo no existe o es inválido, la app mantiene baseline mínimo en consola y continúa operativa.
- Contrato de fallback por entorno:
	- `dev`: human-friendly
	- `test`: human-friendly minimalista
	- `prod`: JSON estructurado

## Enabler EN-0201: In-Memory Database Testing Baseline

El backend incluye baseline explícito para pruebas de integración con persistencia en memoria.

- Activación de testing DB: `TEST_DATABASE_URL` (si está presente) tiene prioridad sobre `DATABASE_URL`.
- Las pruebas de integración de persistencia están en `tests/integration/persistence/`.
- Clasificación de pruebas con marker: `persistence_integration`.
- El esquema se inicializa por migraciones en cada caso de prueba y se aísla con DB en memoria por test.

Ejecutar únicamente la suite de persistencia:

```bash
pytest tests/integration/persistence -m persistence_integration
```
