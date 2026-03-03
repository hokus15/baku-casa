# Research — F-0001 Acceso y Autenticación (Operador)

## 1) Revocación en logout con JWT stateless

- Decision: Implementar logout con revocación explícita del token actual (por identificador de token), manteniendo revocación global por versión de credencial para cambio de contraseña.
- Rationale: Cumple la aclaración funcional de F-0001 y mantiene compatibilidad con ADR-0005 (JWT stateless + `ver`) sin introducir sesiones server-side globales.
- Alternatives considered:
  - Logout solo cliente (descartar token local): rechazado porque no cumple la aclaración acordada.
  - Logout global en cada cierre: rechazado por impacto UX y porque la revocación global ya está reservada al cambio de contraseña.

## 2) Protección contra fuerza bruta

- Decision: Política base de bloqueo temporal tras 5 intentos fallidos consecutivos durante 15 minutos, con ambos parámetros configurables.
- Rationale: Balancea seguridad y operatividad en entorno de operador único, y deja margen de endurecimiento sin cambiar contrato funcional.
- Alternatives considered:
  - Sin límite explícito: rechazado por riesgo de fuerza bruta.
  - Solo backoff progresivo sin bloqueo: rechazado por menor efectividad en abuso repetitivo.
  - Bloqueo indefinido/manual: rechazado por fricción operativa excesiva en MVP.

## 3) Auditoría mínima obligatoria

- Decision: Hacer obligatorios `created_at` y `last_login_at`; `updated_at` obligatorio en el modelo y nullable hasta primera modificación efectiva.
- Rationale: Alinea trazabilidad mínima con F-0001 y con política de UTC de ADR-0012.
- Alternatives considered:
  - Auditoría completamente opcional: rechazada por falta de trazabilidad mínima para autenticación.
  - Exigir `updated_at` no-null desde bootstrap: rechazado porque no refleja semántica de “sin actualización”.

## 4) Contratos y versionado de API

- Decision: Tratar la superficie de autenticación de F-0001 como cambio aditivo no-breaking en MAJOR vigente; definir contract tests para endpoints y errores tipificados.
- Rationale: Cumple ADR-0004/0006 y evita incremento de versión mayor innecesario.
- Alternatives considered:
  - Incrementar MAJOR para introducir auth: rechazado por no existir ruptura incompatible en contratos existentes.
  - Posponer contract tests a fases posteriores: rechazado por incumplir ADR-0006 y ADR-0008.

## 5) Integración multi-root

- Decision: Implementación funcional en root `backend`; `bot` consume el contrato versionado sin imports runtime cruzados.
- Rationale: Respeta ADR-0001 y evita acoplamiento entre roots.
- Alternatives considered:
  - Compartir librería interna de autenticación entre roots: rechazado por violar aislamiento multi-root.

## Resultado de clarificaciones

No quedan `NEEDS CLARIFICATION` abiertos para F-0001.
