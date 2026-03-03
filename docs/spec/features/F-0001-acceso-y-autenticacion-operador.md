# F-0001: Acceso y Autenticación (Operador)

## Objetivo

Restringir el acceso al sistema a un operador autenticado, habilitando el uso seguro del resto de features.

---

## Definiciones

**Operador (usuario del sistema)**: actor autenticado que usa el sistema para gestionar propietarios, propiedades, contratos y contabilidad.

- El operador **no** es un propietario (sujeto fiscal).
- En el MVP existe **un único** operador.

---

## Capacidades

El sistema debe permitir:

- **Bootstrap**: establecer credenciales iniciales del operador (primer arranque).
- **Autenticación**: iniciar sesión con credenciales válidas.
- **Cierre de sesión**: finalizar sesión activa mediante revocación explícita del token actual.
- **Gestión de credenciales**: cambiar contraseña del operador.
- **Revocación**: invalidar sesiones/tokens existentes tras cambio de contraseña (TBD mecanismo exacto).

---

## Reglas de negocio

- Todas las operaciones funcionales del sistema requieren autenticación.
- Un intento de acceso sin autenticar debe ser rechazado.
- El sistema debe implementar protección frente a fuerza bruta mediante bloqueo temporal tras intentos fallidos consecutivos.
- La política mínima de bloqueo será:
  - 5 intentos fallidos consecutivos.
  - Bloqueo durante 15 minutos.
- Los parámetros de intentos máximos y duración del bloqueo deben ser configurables.
- Las credenciales del operador deben poder rotarse (cambio de contraseña).
- Las credenciales del operador deber guardarse encriptadas si se persisten.
- Tras cambio de contraseña, las sesiones/tokens existentes deben quedar revocados.
- El TTL de los tokens debe ser configurable.

---

## Auditoría mínima

El usuario operador debe mantener los siguientes campos de auditoría:

- `created_at` (obligatorio).
- `last_login_at` (obligatorio).
- `updated_at` (obligatorio en el modelo; puede ser `null` hasta que exista una actualización efectiva).

`updated_at` debe establecerse únicamente cuando se produzca una modificación del operador.

---

## Fuera de alcance

- Múltiples usuarios.
- Roles/permisos (RBAC/ACL).
- Invitaciones.
- SSO/OAuth.
- Recuperación de contraseña vía email/SMS.
- Permisos por propietario o por propiedad.

---

## ADR aplicables

### Base
- ADR-0001
- ADR-0002
- ADR-0003
- ADR-0004
- ADR-0005
- ADR-0006
- ADR-0007
- ADR-0008
- ADR-0009
- ADR-0011
- ADR-0012
