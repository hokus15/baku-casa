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

### Alineacion de listados con EN-0202

Esta feature no introduce listados funcionales de dominio como capacidad principal.

Si dentro de su alcance se expone cualquier endpoint de coleccion (por ejemplo, intentos de acceso o sesiones), debe cumplir obligatoriamente la disciplina transversal de paginacion:

- paginacion obligatoria en toda coleccion
- valores por defecto y limites maximos definidos de forma transversal
- parametros de paginacion resueltos exclusivamente mediante el configuration system (EN-0202) con precedencia global: `environment variables > config file > defaults`
- prohibido definir defaults o maximos hardcoded fuera de la configuracion central

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
- ADR-0013

---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Correlacion por request mediante `correlation_id`.

---

## Baseline de testing de persistencia (EN-0201)

Las pruebas de integración de esta feature deben ejecutarse sobre el baseline EN-0201 cuando requieran persistencia:

- DB en memoria activada por configuración de test explícita.
- Inicialización determinista de esquema mediante migraciones.
- Aislamiento de estado entre casos para evitar dependencias temporales entre tests.
