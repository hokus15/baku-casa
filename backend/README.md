# Backend Root

Root independiente del backend para bootstrap EN-0100.

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
