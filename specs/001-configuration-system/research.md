# Research - EN-0202 Configuration System

## Decision 1: Precedencia global fija de fuentes
- Decision: Usar precedencia determinista unica `environment variables > config file > defaults` en todos los entornos.
- Rationale: Alinea ADR-0013, evita deriva entre entornos y simplifica validacion reproducible.
- Alternatives considered:
  - Precedencia por entorno: rechazada por introducir ambiguedad operativa.
  - Precedencia por tipo de clave: rechazada por elevar complejidad y riesgo de incoherencia.

## Decision 2: Claves no declaradas permitidas con warning
- Decision: Permitir claves no declaradas, registrando warning estructurado y visible, sin bloquear arranque por ese motivo.
- Rationale: Mantiene resiliencia operativa frente a ruido de entorno sin perder trazabilidad diagnostica.
- Alternatives considered:
  - Modo estricto con fallo: rechazado para este item por mayor friccion operativa inicial.
  - Ignorar silenciosamente: rechazado por perder capacidad de deteccion temprana.

## Decision 3: Validacion de arranque con agregacion de errores
- Decision: Fallar arranque cuando la configuracion es invalida, reportando el conjunto completo de errores detectados.
- Rationale: Reduce ciclos de correccion y mejora reproducibilidad del troubleshooting.
- Alternatives considered:
  - Fallo en primer error: rechazado por feedback parcial y mas iteraciones.
  - Arranque con errores no criticos: rechazado por contradecir fail-fast de ADR-0013.

## Decision 4: Segmentacion por entorno sin minimos obligatorios especificos
- Decision: Definir requeridos globales; no definir minimos obligatorios separados por `dev/test/prod`.
- Rationale: Conserva contrato de configuracion estable y evita reglas divergentes por entorno.
- Alternatives considered:
  - Minimos por entorno: rechazado por complejidad normativa adicional.

## Decision 5: Fronteras arquitectonicas de consumo
- Decision: Concentrar lectura/resolucion de configuracion en interfaz centralizada consumida por Application/Infrastructure/Interfaces; Domain no depende de configuracion.
- Rationale: Cumple ADR-0002 y ADR-0013, preservando aislamiento del dominio.
- Alternatives considered:
  - Lectura directa de variables de entorno en modulos: rechazada por violar ADR-0013.

## Decision 6: Superficies externas y versionado
- Decision: EN-0202 no introduce cambios en contratos HTTP/eventos ni versionado externo.
- Rationale: El alcance es habilitador interno del root `backend/`.
- Alternatives considered:
  - Exponer contrato externo de configuracion: rechazado por fuera de alcance del roadmap item.

## Dependency Graph Validation
- `EN-0202` depende de `F-0001` y dicha dependencia esta satisfecha (`done`).
- No se requieren enablers/features posteriores para implementar EN-0202.
- No se detectan dependencias implicitas adicionales.

## ADR Gap
- No se requiere crear ni modificar ADR para este item.
- La cobertura normativa principal se encuentra en ADR-0013, complementada por ADR-0001, ADR-0002, ADR-0007 y ADR-0008.

---

## F-0001 Key Inventory and Legacy-to-Centralized Mapping

### Source file
`backend/src/baku/backend/infrastructure/config/auth_settings.py` — `AuthSettings.__init__`

### Auth configuration keys

| Env Var | Default | Type | Required | Centralized Key |
|---|---|---|---|---|
| `AUTH_JWT_SECRET` | none | `str` | YES (no default) | `auth.jwt_secret` |
| `AUTH_JWT_ALGORITHM` | `"HS256"` | `str` | NO | `auth.jwt_algorithm` |
| `AUTH_TOKEN_TTL_SECONDS` | `3600` | `int` | NO | `auth.token_ttl_seconds` |
| `AUTH_MAX_FAILED_ATTEMPTS` | `5` | `int` | NO | `auth.max_failed_attempts` |
| `AUTH_LOCKOUT_MINUTES` | `15` | `int` | NO | `auth.lockout_minutes` |

### Migration strategy
- `AUTH_JWT_SECRET` becomes a **required global key** validated at startup by the centralized validator.
- Remaining keys retain their defaults via the `defaults` source layer.
- `AuthSettings` is refactored to consume the centralized `ConfigurationProviderPort` instead of reading `os.getenv` directly.
- `reset_auth_settings()` test helper is preserved; callers must also reset the centralized provider singleton in tests.
- No external contract changes; HTTP API surfaces are unaffected.
