# Data Model — F-0001 Acceso y Autenticación (Operador)

## Entidades

## 1) Operator

- Description: Usuario único autenticable del sistema.
- Fields:
  - `operator_id` (ID opaco, inmutable)
  - `username` (único)
  - `password_hash` (no reversible)
  - `credential_version` (entero >= 1)
  - `created_at` (UTC, obligatorio)
  - `updated_at` (UTC, nullable hasta primera actualización)
  - `last_login_at` (UTC, obligatorio tras primer login exitoso)
  - `is_active` (booleano)
- Validation Rules:
  - Solo puede existir 1 operador activo para F-0001.
  - `password_hash` nunca puede ser texto plano.
  - `credential_version` se incrementa de forma atómica al cambiar contraseña.
  - `is_active` se establece en `true` en el bootstrap; no tiene transición de estado en MVP.

## 2) RevokedToken

- Description: Registro de revocación explícita del token actual en logout.
- Fields:
  - `token_jti` (único)
  - `operator_id` (FK a Operator)
  - `revoked_at` (UTC)
  - `expires_at` (UTC)
  - `reason` (enum: `logout`)
- Validation Rules:
  - `token_jti` debe ser único para prevenir duplicidad.
  - `expires_at` >= `revoked_at`.
- Lifecycle:
  - Se crea en logout.
  - Puede eliminarse por expiración sin alterar trazabilidad funcional.

## 3) LoginThrottleState

- Description: Estado de control de intentos fallidos de autenticación por operador.
- Fields:
  - `operator_id` (FK único)
  - `failed_attempts` (entero >= 0)
  - `blocked_until` (UTC, nullable)
  - `last_failed_at` (UTC, nullable)
- Validation Rules:
  - `failed_attempts` se resetea tras login exitoso.
  - Bloqueo aplica mientras `blocked_until` sea mayor al tiempo actual UTC.
  - Configuración base: umbral 5, duración 15 min (ambos configurables).

## 4) AuthPolicyConfig

- Description: Parámetros de política de autenticación. **No es una entidad persistida en base de datos**: se gestiona únicamente como configuración de entorno (`auth_settings.py`). No requiere tabla, migración ni repositorio.
- Config keys:
  - `token_ttl_seconds` (entero > 0)
  - `max_failed_attempts` (entero >= 1; base 5)
  - `lockout_minutes` (entero >= 1; base 15)
- Validation Rules:
  - Todos los parámetros deben existir y ser válidos antes de autenticar.

## Relaciones

- `Operator` 1 — N `RevokedToken`
- `Operator` 1 — 1 `LoginThrottleState`

## Transiciones de estado

1. Bootstrap:
   - Precondición: no existe `Operator`.
   - Resultado: se crea `Operator` con `credential_version = 1`.

2. Login exitoso:
   - Precondición: credenciales válidas y no bloqueado.
   - Resultado: emisión de token; actualización de `last_login_at`; reset de `failed_attempts`.

3. Login fallido:
   - Resultado: incremento de `failed_attempts`; si alcanza umbral, se establece `blocked_until`.

4. Logout:
   - Precondición: token válido actual.
   - Resultado: creación de `RevokedToken` con motivo `logout`.

5. Cambio de contraseña:
   - Resultado: actualización de `password_hash`, incremento de `credential_version`, invalidación de tokens previos por mismatch de `ver`.

## Invariantes

- Tiempos en UTC (ADR-0012).
- Errores tipificados para bloqueo, token inválido/expirado/revocado y credenciales inválidas (ADR-0009).
- Sin sesiones server-side globales; revocación principal por `credential_version` y revocación puntual por `token_jti` en logout (ADR-0005).
