# Feature Specification: F-0001 - Acceso y Autenticación (Operador)

**Feature Branch**: `001-acceso-autenticacion-operador`  
**Created**: 2026-03-03  
**Status**: Draft  
**Input**: User description: "Genera la especificación para la F-0001: Acceso y Autenticación (Operador)."

## Clarifications

### Session 2026-03-03

- Q: ¿Qué significa exactamente `logout` en esta feature? → A: Logout con revocación del token actual.
- Q: ¿Qué política mínima de intentos fallidos de login debe exigir esta feature? → A: Bloqueo temporal tras intentos fallidos consecutivos.
- Q: ¿Qué parámetros mínimos tendrá el bloqueo temporal por intentos fallidos? → A: Base 5 intentos y 15 minutos, configurable.
- Q: ¿La auditoría mínima de acceso debe ser obligatoria u opcional? → A: Obligatoria para `last_login_at`,  `created_at` y `updated_at` (`updated_at` obligatorio en el modelo; puede ser `null` hasta que exista una actualización efectiva). `updated_at` debe establecerse únicamente cuando se produzca una modificación del operador.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Bootstrap de credenciales iniciales (Priority: P1)

Como operador único del sistema, necesito establecer mis credenciales iniciales en el primer arranque para que el sistema quede protegido desde el inicio.

**Why this priority**: Sin credenciales iniciales no existe control de acceso y el resto de capacidades del sistema no puede usarse de forma segura.

**Independent Test**: Puede validarse iniciando el sistema sin operador previo, ejecutando el flujo de bootstrap una sola vez y comprobando que queda habilitado el inicio de sesión.

**Acceptance Scenarios**:

1. **Given** que no existe operador inicial registrado, **When** se completa el bootstrap con credenciales válidas, **Then** el operador queda registrado y el sistema exige autenticación para operar.
2. **Given** que ya existe operador inicial registrado, **When** se intenta repetir el bootstrap, **Then** el sistema rechaza la operación con error tipificado.

---

### User Story 2 - Inicio y cierre de sesión (Priority: P1)

Como operador autenticado, necesito iniciar sesión para acceder a funciones del sistema y cerrar sesión cuando termine para reducir exposición de acceso.

**Why this priority**: Este flujo habilita el uso diario del producto y controla el acceso a todas las operaciones funcionales.

**Independent Test**: Puede validarse probando acceso con credenciales válidas e inválidas y verificando que operaciones funcionales no autenticadas son rechazadas.

**Acceptance Scenarios**:

1. **Given** credenciales válidas del operador, **When** solicita inicio de sesión, **Then** recibe un token de acceso con expiración y puede ejecutar operaciones protegidas.
2. **Given** credenciales inválidas, **When** solicita inicio de sesión, **Then** el sistema rechaza el acceso con error tipificado sin filtrar información sensible.
3. **Given** una sesión activa, **When** el operador cierra sesión, **Then** el token actual queda revocado y ya no puede reutilizarse en operaciones protegidas.

---

### User Story 3 - Rotación de contraseña con revocación (Priority: P1)

Como operador, necesito cambiar mi contraseña y revocar accesos emitidos previamente para mantener control de seguridad cuando una credencial deja de ser confiable.

**Why this priority**: La revocación inmediata tras cambio de contraseña es requisito explícito de seguridad y evita reutilización de accesos antiguos.

**Independent Test**: Puede validarse iniciando sesión, cambiando contraseña, y comprobando que tokens previos quedan inválidos y solo las nuevas credenciales permiten acceso.

**Acceptance Scenarios**:

1. **Given** un operador autenticado con token vigente, **When** cambia su contraseña, **Then** sus tokens emitidos antes del cambio quedan revocados.
2. **Given** tokens revocados por cambio de contraseña, **When** se usan en operaciones protegidas, **Then** el sistema responde con rechazo de autenticación.
3. **Given** la contraseña nueva válida, **When** el operador inicia sesión otra vez, **Then** obtiene acceso con nuevos tokens vigentes.

### Edge Cases

- Intentos repetidos de bootstrap después de completar el primer arranque.
- Uso de token expirado en una operación protegida.
- Uso concurrente de token antiguo durante una operación de cambio de contraseña.
- Solicitudes sin token o con token malformado.
- Uso de credenciales antiguas inmediatamente después de una rotación de contraseña.
- Reintento de uso de un token explícitamente cerrado por logout.
- Intentos de inicio de sesión repetidos con credenciales inválidas hasta activar bloqueo temporal.
- Intento de autenticación durante ventana activa de bloqueo temporal.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST permitir bootstrap de credenciales iniciales del operador únicamente cuando no exista operador previamente configurado.
- **FR-002**: El sistema MUST rechazar cualquier segundo intento de bootstrap una vez inicializado el operador.
- **FR-003**: El sistema MUST autenticar al operador mediante credenciales válidas y emitir un token con tiempo de expiración.
- **FR-004**: El sistema MUST requerir autenticación para toda operación funcional del sistema.
- **FR-005**: El sistema MUST rechazar acceso sin autenticación o con token inválido, expirado o revocado, devolviendo error tipificado.
- **FR-006**: El sistema MUST permitir cierre de sesión de una sesión activa revocando el token actual.
- **FR-007**: El sistema MUST permitir rotación de contraseña del operador autenticado.
- **FR-008**: El sistema MUST invalidar tokens/sesiones previos al cambio de contraseña de forma inmediata.
- **FR-009**: El sistema MUST mantener un valor de TTL de token configurable.
- **FR-010**: Si se persisten credenciales, el sistema MUST almacenarlas en forma no reversible (nunca en texto plano).
- **FR-011**: El sistema MUST registrar errores de autenticación con código estable en inglés y mensaje al usuario en español.
- **FR-012**: El sistema MUST registrar y propagar identificador de correlación en respuestas de error de autenticación.
- **FR-013**: Los timestamps de autenticación y auditoría MUST manejarse en UTC y formato temporal consistente.
- **FR-014**: El sistema MUST mantener el alcance de usuario único (operador único) en esta feature.
- **FR-015**: El sistema MUST dejar explícitamente fuera de alcance RBAC, múltiples usuarios, SSO/OAuth e invitaciones en esta versión.
- **FR-016**: El sistema MUST aplicar bloqueo temporal tras intentos fallidos consecutivos de autenticación; la configuración base es 5 intentos y 15 minutos de bloqueo, ambos valores configurables.
- **FR-017**: El umbral de intentos fallidos y la duración del bloqueo temporal MUST ser configurables.
- **FR-019**: Durante el bloqueo temporal, el sistema MUST rechazar nuevos intentos de autenticación del operador con error tipificado.
- **FR-020**: El sistema MUST registrar `last_login_at` del operador en cada autenticación exitosa.
- **FR-021**: El sistema MUST registrar `created_at` y `updated_at` del operador. `updated_at` es obligatorio en el modelo y puede ser `null` hasta que se produzca una modificación efectiva del registro.

### Constitution Alignment *(mandatory)*

- **CA-001 (Layer boundaries)**: Impacta reglas de autenticación, manejo de sesión/token y errores tipificados en límites de aplicación e interfaz; no introduce excepciones a separación de capas.
- **CA-002 (Contract surface)**: La superficie contractual HTTP cambia al incorporar flujos de bootstrap, login, logout y cambio de contraseña; los cambios se consideran aditivos y compatibles dentro de la versión mayor vigente.
- **CA-003 (Contract tests)**: Deben existir pruebas de contrato para flujos de autenticación y para estabilidad del esquema de errores de autenticación.
- **CA-004 (Financial/time invariants)**: Sin impacto monetario ni de porcentajes; sí hay impacto temporal y se exige UTC para expiración, emisión y auditoría.
- **CA-005 (Documentation impact)**: Esta especificación documenta comportamiento de F-0001; no se identifica cambio estructural que requiera nuevo ADR.

### Key Entities *(include if feature involves data)*

- **Operador**: Usuario único del sistema con identidad autenticable y estado activo para acceso a operaciones protegidas.
- **Credencial de Operador**: Conjunto de datos de autenticación del operador, incluyendo secreto no reversible y metadatos de vigencia.
- **Versión de Credencial**: No es una entidad separada. Es el campo `credential_version` (entero) del `Operator`, que se incrementa atómicamente al cambiar contraseña e invalida todos los tokens emitidos bajo el valor anterior.
- **Token de Acceso**: Credencial temporal de sesión con identidad del operador, tiempo de emisión y expiración.
- **Evento de Auditoría de Acceso**: Concepto lógico implementado como campos de `Operator`, no como entidad separada. `last_login_at` es obligatorio; `created_at` y `updated_at` son obligatorios en el modelo (`updated_at` puede ser `null` hasta primera modificación efectiva).

### Assumptions

- El sistema opera en modo operador único durante todo el MVP 1.
- El acceso a operaciones funcionales se realiza por interfaces contractuales versionadas ya existentes del producto.
- La revocación por cambio de contraseña aplica a todos los tokens emitidos bajo la versión de credencial anterior.

### ADR Impactados Materialmente

- **ADR-0004**: Se amplía la superficie contractual HTTP con flujos de autenticación bajo versionado mayor estable.
- **ADR-0005**: Se aplican autenticación por token, expiración configurable y revocación tras cambio de contraseña.
- **ADR-0006**: Hay impacto en contratos de integración por incorporación de nuevas capacidades de autenticación.
- **ADR-0009**: Se requiere modelo de error tipificado, mensajes en español, códigos estables y correlación.
- **ADR-0012**: Se exige manejo temporal en UTC para emisión/expiración de tokens y campos de auditoría.

### ADR Gap

No se identifica necesidad de crear ni modificar ADR para esta feature; los ADR vigentes cubren el alcance definido.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de operaciones funcionales protegidas rechaza solicitudes no autenticadas en pruebas de aceptación.
- **SC-002**: El operador puede completar bootstrap inicial y primer inicio de sesión exitoso en menos de 3 minutos en entorno local.
- **SC-003**: El 100% de tokens emitidos antes de un cambio de contraseña quedan inválidos inmediatamente después del cambio en pruebas de revocación.
- **SC-004**: Al menos el 95% de intentos de autenticación válidos completan acceso en menos de 2 segundos en condiciones normales de operación local.
  > **Nota (MVP)**: SC-004 es un objetivo operativo, no un criterio automatizado en MVP. No existe benchmark automatizado en la suite de tests inicial. La validación de p95 < 2s se realizará mediante observación operacional. Mejora post-MVP: añadir benchmark de latencia al pipeline de CI.
- **SC-005**: El 100% de respuestas de error de autenticación incluyen código estable y mensaje en español con identificador de correlación.
- **SC-006**: El 100% de secuencias de intentos fallidos por encima del umbral configurado activa bloqueo temporal verificable en pruebas de aceptación.
