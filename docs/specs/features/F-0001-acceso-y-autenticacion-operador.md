# F-0001: Acceso y Autenticación (Operador)

---

## Objetivo

Restringir el acceso al sistema a un operador autenticado, habilitando el uso seguro del resto de features.

---

## Alcance

Esta feature cubre:

- **Bootstrap**: establecer credenciales iniciales del operador (primer arranque).
- **Autenticación**: iniciar sesión con credenciales válidas.
- **Cierre de sesión**: finalizar sesión activa mediante revocación explícita del token actual.

---

## Fuera de alcance

- Múltiples usuarios.
- Roles/permisos (RBAC/ACL).
- Invitaciones.
- SSO/OAuth.
- Recuperación de contraseña vía email/SMS.
- Permisos por propietario o por propiedad.

---

## Definiciones

**Operador (usuario del sistema)**: actor autenticado que usa el sistema para gestionar propietarios, propiedades, contratos y contabilidad.

- El operador **no** es un propietario (sujeto fiscal).
- En el MVP existe **un único** operador.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Operador (usuario del sistema)
- Ver definiciones de dominio y datos principales de la feature

---

## Datos principales

La feature gestiona la siguiente información:

### Auditoría mínima

El usuario operador debe mantener metadatos mínimos de auditoría para creación, actualización y último acceso:

- fecha de creación (obligatoria)
- fecha de último acceso correcto (obligatoria)
- fecha de última actualización efectiva (obligatoria en el modelo, aunque inicialmente pueda no tener valor)

La fecha de última actualización efectiva debe establecerse únicamente cuando se produzca una modificación del operador.

---

## Capacidades

El sistema debe permitir:

- **Bootstrap**: establecer credenciales iniciales del operador (primer arranque).
- **Autenticación**: iniciar sesión con credenciales válidas.
- **Cierre de sesión**: finalizar sesión activa mediante revocación explícita del token actual.
- **Gestión de credenciales**: cambiar contraseña del operador.
- **Revocación**: invalidar todas las sesiones/tokens activos del operador tras cambio de contraseña.

---

## Reglas del dominio

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

Si dentro de su alcance se expone cualquier endpoint de coleccion (por ejemplo, intentos de acceso o sesiones), debe cumplir el contrato comun definido en:

- docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Todas las operaciones funcionales del sistema requieren autenticación.
- Un intento de acceso sin autenticar debe ser rechazado.
- El sistema debe implementar protección frente a fuerza bruta mediante bloqueo temporal tras intentos fallidos consecutivos.

---

## Dependencias

Esta feature puede depender de:

- EN-0100

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0003-api-response-conventions.md
- docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- **Bootstrap**: establecer credenciales iniciales del operador (primer arranque).
- **Autenticación**: iniciar sesión con credenciales válidas.
- **Cierre de sesión**: finalizar sesión activa mediante revocación explícita del token actual.

---


### Baseline de testing de persistencia (EN-0201)

Las pruebas de integración de esta feature deben ejecutarse sobre el baseline EN-0201 cuando requieran persistencia:

- DB en memoria activada por configuración de test explícita.
- Inicialización determinista de esquema mediante migraciones.
- Aislamiento de estado entre casos para evitar dependencias temporales entre tests.

---
