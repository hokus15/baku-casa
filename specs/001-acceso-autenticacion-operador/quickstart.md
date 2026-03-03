# Quickstart — F-0001 Acceso y Autenticación (Operador)

## Objetivo

Validar el comportamiento funcional de bootstrap, autenticación, logout con revocación,
rotación de contraseña y bloqueo temporal por intentos fallidos.

## Prerrequisitos

- Root `backend` disponible.
- Base de datos en estado limpio para validar bootstrap.
- Configuración de autenticación cargada (incluyendo TTL y parámetros de bloqueo).

## Flujo de validación manual

1. Bootstrap inicial
   - Ejecutar bootstrap con credenciales válidas.
   - Verificar que un segundo bootstrap es rechazado con error tipificado.

2. Login
   - Iniciar sesión con credenciales válidas y obtener token.
   - Ejecutar operación protegida y verificar acceso.

3. Logout con revocación explícita
   - Cerrar sesión con token vigente.
   - Reutilizar ese mismo token y verificar rechazo por revocación.

4. Rotación de contraseña
   - Iniciar sesión de nuevo y cambiar contraseña.
   - Reutilizar token anterior al cambio y verificar rechazo por revocación global (`ver`).
   - Iniciar sesión con contraseña nueva y verificar éxito.

5. Bloqueo temporal por fallos
   - Realizar intentos fallidos consecutivos hasta umbral.
   - Verificar activación de bloqueo temporal y rechazo de nuevos intentos durante la ventana.
   - Ajustar configuración para validar que umbral/duración son configurables.

6. Auditoría mínima
   - Verificar `created_at` al bootstrap.
   - Verificar `last_login_at` en login exitoso.
   - Verificar `updated_at` nullable al inicio y actualizado al modificar operador.

## Validación de calidad (CI)

En PR de F-0001 deben pasar al menos:

- `lint`
- `type-check`
- `smoke tests` por root
- pruebas de contrato de autenticación (si aplica cambio de superficie HTTP)

## Resultado de validación — F-0001 implementación completa

**Fecha de validación**: 2026-03-03 (implementación inicial)

**Método de validación**: Suite de tests automática (34 tests).

| Escenario | Resultado |
|---|---|
| Bootstrap inicial → 201 | ✅ PASS |
| Bootstrap repetido → 409 `AUTH_BOOTSTRAP_ALREADY_COMPLETED` | ✅ PASS |
| Login con credenciales válidas → token JWT | ✅ PASS |
| Login con credenciales inválidas → 401 `AUTH_INVALID_CREDENTIALS` | ✅ PASS |
| N intentos fallidos → bloqueo temporal 429 `AUTH_LOCKED_TEMPORARILY` | ✅ PASS |
| Logout → 204; reutilización revocada `AUTH_TOKEN_REVOKED` | ✅ PASS |
| Doble logout idempotente → 401 `AUTH_TOKEN_REVOKED` | ✅ PASS |
| Cambio de contraseña → tokens anteriores rechazados (`ver`) | ✅ PASS |
| Login con contraseña nueva → acceso exitoso | ✅ PASS |
| `last_login_at` actualizado en login exitoso | ✅ PASS |
| `updated_at` nullable al inicio; actualizado al cambiar contraseña | ✅ PASS |
| `correlation_id` presente en todas las respuestas de error | ✅ PASS |

**CI gates ejecutados**:
```bash
ruff check src/ tests/   # All checks passed
mypy src/                 # Success: no issues found in 40 source files
pytest tests/ -q          # 35 passed in 29.77s
```
