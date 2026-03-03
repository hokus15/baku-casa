# Backend Root

Root independiente del backend para bootstrap EN-0100.

## Alcance
- Solo estructura mínima (`pyproject`, `src`, `tests`).
- Sin endpoints reales.
- Sin lógica de dominio.
- Sin migraciones ni eventos.

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

### Dependencias de producción

| Paquete | Propósito |
|---|---|
| `fastapi` | HTTP adapter (ADR-0004) |
| `uvicorn[standard]` | ASGI server |
| `PyJWT` | Tokens JWT stateless (ADR-0005) |
| `bcrypt` | Hash de contraseñas (sin passlib) |
| `SQLAlchemy` | ORM + SQLite (ADR-0003) |
