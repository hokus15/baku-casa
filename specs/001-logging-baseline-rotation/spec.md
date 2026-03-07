# Feature Specification: EN-0200 - Application Logging Baseline with Daily Rotation

**Feature Branch**: `001-logging-baseline-rotation`  
**Created**: 2026-03-07  
**Status**: Draft  
**Input**: User description: "Genera la especificacion para el Roadmap Item EN-0200: Application Logging Baseline with Daily Rotation"

## Clarifications

### Session 2026-03-07

- Q: Como se interpreta exactamente la retencion de logs en doble salida (JSON + human-friendly)? -> A: Retencion inicial de 7 dias para logs rotados, configurable por entorno, manteniendo ficheros activos.
- Q: Que conjunto de features existentes debe sincronizarse por impacto de EN-0200? -> A: Actualizar todas las features existentes en `docs/spec/features/` para unificar observabilidad.
- Q: Como debe organizarse la configuracion del framework de logging por entorno? -> A: En ficheros especificos del framework ubicados en la raiz de `backend/`, uno por entorno (`dev`, `test`, `prod`).
- Q: Que hacer si falta o es invalido el fichero del entorno activo? -> A: Aplicar fallback seguro del framework manteniendo baseline minimo obligatorio de logging (sin modo "sin logging") y sin bloquear el arranque de la aplicacion.
- Q: Cual es el contrato de fallback por entorno? -> A: En fallback se escribe por consola con baseline minimo obligatorio: `dev` salida human-friendly, `test` salida human-friendly minimalista para testabilidad, `prod` salida estructurada JSON.
- Q: Cual es el rol de la aplicacion respecto al framework de logging? -> A: Solo cargar el fichero de perfil del framework y dejar que handlers/formatters/loggers del framework gobiernen el comportamiento.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnostico tecnico consistente (Priority: P1)

Como operador del backend, quiero que todos los flujos relevantes emitan logs estructurados
consistentes para poder diagnosticar errores y ejecuciones sin depender de mensajes libres.

**Why this priority**: Es la capacidad base de observabilidad definida por la constitucion y
habilita soporte operativo del resto del roadmap.

**Independent Test**: Puede validarse ejecutando flujos de referencia (incluyendo F-0001 y
EN-0202) y comprobando que cada evento relevante produce registros con los campos
obligatorios y mensajes tecnicos en ingles.

**Acceptance Scenarios**:

1. **Given** una operacion tecnica relevante del backend, **When** se genera un evento de
   logging, **Then** el registro incluye al menos `timestamp` en UTC, `level`,
   `service_name`, `correlation_id` y `message`.
2. **Given** un error tipificado en una operacion del backend, **When** se registra el
   fallo, **Then** el log conserva `correlation_id` y contexto diagnostico sin exponer
   secretos ni PII por defecto.

---

### User Story 2 - Trazabilidad de ejecucion extremo a extremo (Priority: P2)

Como operador, quiero correlacionar en logs todas las entradas de una misma ejecucion para
poder reconstruir el flujo tecnico y reducir tiempo de investigacion.

**Why this priority**: La correlacion es requisito constitucional y de ADR-0009 para
observabilidad y soporte de incidencias.

**Independent Test**: Puede probarse enviando solicitudes independientes y verificando que
cada una mantiene su `correlation_id` en todos los registros del flujo.

**Acceptance Scenarios**:

1. **Given** una solicitud entrante con `correlation_id`, **When** la solicitud atraviesa
   los pasos del flujo, **Then** todos los logs asociados preservan ese mismo
   `correlation_id`.
2. **Given** una solicitud sin `correlation_id` previo, **When** el backend la procesa,
   **Then** se genera uno y se usa consistentemente durante toda la ejecucion.

---

### User Story 3 - Operacion diaria con rotacion controlada (Priority: P3)

Como responsable operativo, quiero que los ficheros de log roten diariamente y tengan
retencion inicial de 7 dias configurable para mantener trazabilidad sin crecimiento
descontrolado.

**Why this priority**: Controla el riesgo operativo en despliegues self-hosted y evita
degradacion por acumulacion de ficheros.

**Independent Test**: Puede validarse simulando el cruce de medianoche Europe/Madrid y
verificando que el sistema crea ficheros nuevos, conserva eventos y aplica la politica de
retencion declarada.

**Acceptance Scenarios**:

1. **Given** logging activo durante el cambio diario, **When** llega las 00:00 en
   Europe/Madrid, **Then** el sistema rota automaticamente los ficheros y continua
   registrando sin perder eventos.
2. **Given** historico de ficheros rotados superior al limite permitido, **When** se
  ejecuta la siguiente rotacion diaria, **Then** el sistema aplica la ventana de retencion
  configurada (valor inicial 7 dias) para ambas salidas, mantiene los ficheros activos y
  elimina excedentes segun la politica declarada.

### Edge Cases

- Registros emitidos alrededor del cambio de horario (DST) en Europe/Madrid.
- Solicitudes concurrentes con diferentes `correlation_id` en el mismo segundo.
- Errores tecnicos durante la escritura de logs sin detener operaciones no relacionadas.
- Mensajes con datos potencialmente sensibles que deben ser excluidos por defecto.
- Alto volumen puntual de eventos durante una misma ventana de rotacion.
- Fichero dedicado de logging ausente, inaccesible o invalido para el entorno activo.
- Perfil de logging configurado para reducir verbosidad sin romper el runtime de la aplicacion, preservando siempre el baseline minimo obligatorio de logging.

## Assumptions

- El alcance operativo de EN-0200 se limita al root `backend/`.
- Aunque EN-0200 depende de EN-0202 en el DAG, este enabler define y crea la configuracion
  especifica del framework de logging requerida para su propio comportamiento como
  configuracion operativa externa en la raiz de `backend/`.
- F-0001 ya esta implementada y debe alinearse al baseline de logging como parte de este
  enabler, sin alterar su alcance funcional.
- No se introducen agregadores externos de logs ni trazado distribuido en este item.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST establecer un baseline unico de logging para `backend/` con
  formato estructurado y esquema de campos estable.
- **FR-002**: Todo registro MUST incluir como minimo `timestamp` (UTC, ISO-8601),
  `level`, `service_name`, `correlation_id` y `message`.
- **FR-003**: Los mensajes tecnicos en logs MUST estar en ingles y los nombres de campos
  MUST ser consistentes en formato `snake_case`.
- **FR-004**: El sistema MUST permitir adjuntar campos contextuales diagnosticos como
  pares estructurados, evitando concatenar todo el contexto dentro de `message`.
- **FR-005**: El sistema MUST persistir logs en fichero en despliegues self-hosted del
  backend.
- **FR-006**: El baseline de logging MUST definirse en ficheros de configuracion del
  framework de logging por entorno, con un fichero dedicado distinto para `dev`, `test`
  y `prod`, ubicados en la raiz de `backend/`.
- **FR-007**: La configuracion del framework de logging (niveles, destinos de salida,
  rotacion y retencion) MUST declararse en dichos ficheros y MUST NOT quedar embebida en
  codigo.
- **FR-008**: Si el fichero dedicado de logging del entorno activo falta o es invalido,
  el sistema MUST aplicar una configuracion fallback segura del framework y mantener la
  aplicacion operativa. El fallback MUST escribir en consola y MUST preservar baseline
  minimo obligatorio de logging; el fallback sin logging esta prohibido.
- **FR-009**: La rotacion de ficheros MUST ejecutarse diariamente a las 00:00 de
  Europe/Madrid sin alterar la regla de timestamps en UTC dentro de cada evento.
- **FR-010**: El sistema MUST definir y aplicar una politica de retencion automatica de
  logs para salidas rotadas con valor inicial de 7 dias, configurable por entorno,
  ademas de conservar los ficheros activos del dia en curso.
- **FR-011**: El sistema MUST registrar eventos de inicio/fin de operaciones relevantes y
  errores en los flujos existentes de EN-0202 y F-0001, con correlacion trazable.
- **FR-012**: Los logs MUST excluir por defecto secretos, tokens, contrasenas y PII no
  necesaria para diagnostico tecnico.
- **FR-013**: El sistema MUST mantener continuidad operativa del logging durante rotacion,
  evitando perdida silenciosa de eventos relevantes.
- **FR-014**: Esta especificacion MUST no introducir cambios en contratos HTTP ni
  contratos de eventos publicados.

### Constitution Alignment *(mandatory)*

- **CA-001**: Impacto de capas: capacidad transversal de observabilidad en bordes e
  infraestructura; Domain permanece libre de dependencias de logging.
- **CA-002**: Impacto contractual externo: `none` (sin cambios en API HTTP ni contratos de
  eventos); impacto de versionado: `none`.
- **CA-003**: Al no haber cambios contractuales, no se requieren nuevos contract tests de
  versionado; se requieren pruebas de comportamiento de logging y correlacion.
- **CA-004**: Invariantes financieros: sin cambios. Invariantes temporales: se mantiene
  timestamp en UTC y rotacion diaria en Europe/Madrid conforme a constitucion y ADR-0012.
- **CA-005**: Impacto documental: requiere actualizacion de documentacion operativa y de
  especificaciones funcionales afectadas; no requiere nuevo ADR si se mantiene dentro de
  ADR vigentes.
- **CA-006**: La implementacion funcional derivada MUST seguir TDD (red -> green ->
  refactor) con evidencia en PR.
- **CA-007**: No se detecta `ADR Gap` para EN-0200; existe cobertura en ADR-0009
  (observabilidad), ADR-0012 (tiempo) y ADR-0013 (configuracion).

### Configuration Artifact

- **Logging Framework Configuration File (per environment)**: Artefacto de configuracion
  del framework de logging para `dev`, `test` y `prod`, ubicado en la raiz de
  `backend/` y no embebido en codigo.
- **Required capabilities in that artifact**:
  - doble salida (estructurada y human-friendly)
  - campos obligatorios en eventos de log
  - rotacion diaria 00:00 Europe/Madrid
  - retencion basada en dias (valor inicial 7), configurable por entorno, con
    preservacion de ficheros activos
  - contrato de fallback por entorno con escritura en consola:
    - `dev`: consola human-friendly
    - `test`: consola human-friendly minimalista
    - `prod`: consola JSON estructurada

## Dependency Graph Impact

- Item objetivo: `EN-0200` (`planned`, `MVP0`).
- Dependencia declarada en `docs/spec/dependency-graph.yaml`: `EN-0202`.
- Verificacion DAG: la especificacion respeta la dependencia previa requerida y no exige
  items posteriores para ser valida.
- Dependientes transitivos identificados en `docs/spec/features/`: `F-0014`
  (via `EN-0208` -> `EN-0200`).
- Impacto en features existentes por este enabler:
  - Deben actualizarse todas las features existentes bajo `docs/spec/features/` para
    explicitar alineacion con el baseline de observabilidad de EN-0200 cuando aplique
    (campos obligatorios, `correlation_id`, mensajes tecnicos en ingles, exclusion de
    datos sensibles y disciplina temporal UTC).
  - La actualizacion completa incluye como minimo `F-0001` a `F-0015`, preservando alcance
    funcional de cada feature y sin introducir cambios de implementacion.
- Dependencias implicitas nuevas: none.

## ADR Impact

- ADR materialmente impactados:
  - `ADR-0009` (modelo de errores y observabilidad).
  - `ADR-0012` (politica temporal UTC y consistencia de timestamps).
  - `ADR-0013` (configuracion tipada para parametros de logging/retencion por entorno).
  - `ADR-0002` (logging como concern transversal sin contaminar Domain).
- ADR no materialmente impactados: sin cambios normativos requeridos.
- Requiere nuevo ADR o modificacion de ADR existente: no.

## ADR Gap

- No se identifica gap normativo para este item.

## Architectural Impact

- HTTP contracts: none.
- Event contracts: none.
- Persistence: changed (persistencia operativa de logs en fichero y rotacion diaria).
- Configuration: changed (fichero especifico de logging y creacion de parametros
  dedicados en el framework de logging para niveles, salidas, rotacion y retencion
  inicial de 7 dias configurable).
- Error model: none (sin nuevas categorias de error publico; se refuerza trazabilidad).
- Versioning impact: none (sin impacto contractual en version mayor/menor).

## Documentation Synchronization

- Documentos a actualizar cuando EN-0200 se implemente:
  - `README.md` (seccion de observabilidad y politica de logs).
  - `backend/README.md` (campos obligatorios, correlacion, rotacion y retencion).
  - Todas las features existentes en `docs/spec/features/` (alineacion transversal con
    baseline de observabilidad EN-0200 segun el contexto de cada feature).
- Documentos sin cambios obligatorios por este alcance:
  - `bot/README.md`
  - `frontend/README.md`
- Sincronizacion de estado de roadmap (si cambia estado del item):
  - actualizar `docs/spec/roadmap.md`
  - actualizar `docs/spec/dependency-graph.yaml`
  - estados permitidos: `planned`, `in_progress`, `done`

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los eventos de logging verificados en flujos de EN-0202 y F-0001
  incluyen todos los campos obligatorios del baseline.
- **SC-002**: En validaciones de trazabilidad, el 100% de solicitudes analizadas mantienen
  un `correlation_id` consistente en todos los registros de su ejecucion.
- **SC-003**: En pruebas operativas de cambio diario, la rotacion ocurre en 00:00
  Europe/Madrid en el 100% de ejecuciones verificadas sin perdida de eventos relevantes.
- **SC-004**: En pruebas de retencion, despues de cada rotacion el sistema conserva
  logs rotados dentro de la ventana configurada (valor inicial 7 dias) para ambas salidas
  y mantiene ficheros activos en el 100% de ejecuciones verificadas.
- **SC-005**: En pruebas de arranque, el 100% de ejecuciones con fichero de logging
  faltante/invalido aplican fallback seguro del framework y mantienen operacion del
  backend.
- **SC-007**: En pruebas de fallback por entorno, el 100% de ejecuciones registran en
  consola conforme al contrato (`dev` human-friendly, `test` human-friendly minimalista,
  `prod` JSON estructurado) manteniendo campos minimos obligatorios.
- **SC-006**: En auditorias de seguridad sobre muestras de logs, 0 registros contienen
  secretos/tokens/contrasenas y al menos el 95% de incidencias tecnicas pueden
  diagnosticarse usando solo los campos estructurados definidos.
