# Feature Specification: EN-0201 - In-Memory Database Testing Baseline

**Feature Branch**: `001-inmemory-db-testing`  
**Created**: 2026-03-07  
**Status**: Draft  
**Input**: User description: "Genera la especificación para el Roadmap Item EN-0201: In-Memory Database Testing Baseline"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pruebas de integración aisladas (Priority: P1)

Como equipo de desarrollo, queremos ejecutar pruebas de integración con persistencia en memoria para validar comportamiento real de repositorios y transacciones sin depender de servicios externos.

**Why this priority**: Es el núcleo del enabler y habilita feedback rápido y reproducible en desarrollo local y CI.

**Independent Test**: Puede validarse ejecutando una suite de integración con persistencia en memoria y comprobando que todas las pruebas pasan sin requerir infraestructura externa.

**Acceptance Scenarios**:

1. **Given** una suite de pruebas de integración de persistencia, **When** se ejecuta en modo testing, **Then** utiliza un backend de base de datos en memoria y no requiere servicios externos.
2. **Given** dos ejecuciones consecutivas de la misma suite, **When** se completan ambas, **Then** producen resultados consistentes y sin dependencia del estado de ejecuciones previas.

---

### User Story 2 - Esquema determinista para tests (Priority: P2)

Como equipo de desarrollo, queremos que el esquema usado por pruebas con DB se inicialice de forma determinista para evitar falsos positivos/negativos por drift estructural.

**Why this priority**: Sin esquema determinista, la fiabilidad del baseline de testing queda comprometida.

**Independent Test**: Puede validarse ejecutando tests de integración en un entorno limpio y verificando que inicializan esquema correcto de forma automática antes de correr casos.

**Acceptance Scenarios**:

1. **Given** una ejecución de tests de integración con DB en memoria, **When** comienza la suite, **Then** el esquema queda inicializado de forma consistente con el modelo persistente esperado para pruebas.
2. **Given** una ejecución repetida en un entorno limpio, **When** se vuelve a inicializar el esquema, **Then** el resultado estructural es equivalente y estable entre ejecuciones.

---

### User Story 3 - Configuración de testing segura y separada (Priority: P3)

Como equipo de desarrollo, queremos una configuración de testing explícita y separada del runtime normal para evitar ejecuciones accidentales de tests contra entornos persistentes.

**Why this priority**: Reduce riesgo operativo y protege datos persistentes fuera del contexto de pruebas.

**Independent Test**: Puede validarse comprobando que las pruebas con DB solo se ejecutan bajo configuración de testing explícita y que dicha configuración no se aplica al runtime normal.

**Acceptance Scenarios**:

1. **Given** una ejecución de la aplicación en runtime normal, **When** inicia fuera de contexto de testing, **Then** no utiliza configuración de DB en memoria para pruebas.
2. **Given** una ejecución de pruebas con DB, **When** se activa configuración de testing explícita, **Then** el sistema aplica exclusivamente parámetros de testing y evita ambigüedad con dev/prod.

### Edge Cases

- Ejecución paralela de pruebas que comparten recursos de persistencia de test.
- Fallo durante la inicialización de esquema antes de ejecutar casos de prueba.
- Interrupción de ejecución de suite que deja estado parcial en el contexto de test.
- Intento de ejecutar pruebas con configuración incompleta o no declarada para testing.
- Diferencias de entorno entre local y CI que podrían alterar orden o aislamiento de casos.

## Assumptions

- EN-0202 ya está integrado y permite configuración de testing explícita para este enabler.
- El alcance operativo de EN-0201 se limita al root `backend/`.
- Este enabler no introduce nuevas capacidades de dominio ni altera contratos externos.
- Las suites de pruebas con DB seguirán ejecutándose dentro del pipeline de calidad definido por ADR-0008.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST ofrecer un modo de testing con persistencia en memoria para pruebas de integración del root `backend/`.
- **FR-002**: El sistema MUST inicializar de forma determinista el esquema requerido por pruebas con DB antes de ejecutar casos de integración que dependan de persistencia.
- **FR-003**: El sistema MUST garantizar aislamiento entre pruebas con DB para que ningún caso dependa de estado persistente generado por otro caso.
- **FR-004**: El sistema MUST definir una configuración de testing explícita y separada del runtime normal para habilitar el modo DB en memoria.
- **FR-005**: El sistema MUST impedir ambigüedad operativa entre configuración de testing y configuración de entornos no testing.
- **FR-006**: La ejecución de pruebas con DB MUST realizarse sin dependencias externas adicionales.
- **FR-007**: El baseline MUST definir convenciones de identificación y ubicación para pruebas de integración con DB dentro de `backend/tests/`.
- **FR-008**: El baseline MUST definir un mecanismo de clasificación de pruebas que permita distinguir pruebas unitarias y de integración con DB cuando corresponda.
- **FR-009**: El baseline MUST ser compatible con ejecución reproducible tanto en entorno local como en CI.
- **FR-010**: La activación de este baseline MUST no alterar el comportamiento funcional ni la configuración de runtime normal fuera del contexto de testing.

### Constitution Alignment *(mandatory)*

- **CA-001**: Impacto de capas: aplica a infraestructura/configuración de pruebas; Domain y Application mantienen desacoplamiento de detalles de persistencia de test.
- **CA-002**: Impacto de contratos externos: `none` (sin cambios HTTP/eventos); impacto de versionado: `none`.
- **CA-003**: No se requieren nuevos contract tests por cambio de contrato; sí se requieren pruebas de integración de persistencia bajo baseline en memoria.
- **CA-004**: Invariantes monetarios/porcentajes/UTC: sin cambios semánticos; este enabler afecta capacidad de prueba, no reglas de negocio.
- **CA-005**: Impacto documental: requiere actualización de documentación de pruebas y de especificaciones funcionales afectadas por baseline de testing; no requiere nuevo ADR si se mantiene dentro de ADR vigentes.
- **CA-006**: Los cambios funcionales derivados MUST seguir TDD (rojo -> verde -> refactor) con evidencia en PR.
- **CA-007**: No se detecta brecha constitucional sin cobertura ADR para este alcance.

### Configuration Artifacts

- **Testing Persistence Profile**: contexto de configuración de pruebas que define ejecución segura y aislada para integración con DB en memoria.
- **Test Schema Lifecycle Rules**: reglas del ciclo de vida del esquema en pruebas (inicialización determinista, uso durante suite/caso y limpieza/aislamiento posterior).
- **DB Integration Test Classification**: convención de clasificación para distinguir pruebas unitarias y de integración con persistencia.

## Dependency Graph Impact

- Item objetivo: `EN-0201` (`planned`, `MVP0`).
- Dependencia declarada: `EN-0202` (`done`) y es suficiente para este alcance.
- El enabler no requiere features/enablers posteriores del roadmap para definirse.
- No se detectan dependencias implícitas nuevas no declaradas en el DAG.
- Por `affects_future_features: true`, el baseline de EN-0201 debe considerarse aplicable a features de `backend/` que usen persistencia en su fase de implementación y validación.

## ADR Impact

- **ADR-0002 (Hexagonal Architecture)**: mantiene separación de capas; pruebas de persistencia no trasladan lógica de negocio a adaptadores.
- **ADR-0003 (Persistence Strategy)**: alineado con baseline de pruebas de integración sobre persistencia en memoria y esquema determinista.
- **ADR-0008 (CI and Governance)**: refuerza disciplina de pruebas de integración reproducibles en CI.
- **ADR-0013 (Configuration System)**: requiere configuración de testing explícita, aislada y no ambigua frente a runtime normal.

## ADR Gap

- No se identifica necesidad de crear o modificar ADR para el alcance actual de EN-0201.

## Architectural Impact

- HTTP contracts: `none`.
- Event contracts: `none`.
- Persistence: `changed` (capacidad de testing con DB en memoria y esquema determinista para pruebas).
- Configuration: `changed` (perfil/configuración de testing separada y explícita).
- Error model: `none` (sin cambios contractuales en tipado de errores públicos).
- Versioning impact: `none`.

## Documentation Synchronization

- Documentación a actualizar durante implementación de EN-0201:
  - `backend/README.md` (modo de testing, aislamiento y convenciones de pruebas con DB).
  - `README.md` (estado del roadmap y baseline técnico de testing).
  - Features existentes en `docs/spec/features/` con alcance `backend` para incorporar referencia al baseline de pruebas con DB en memoria cuando aplique.
- Si cambia el estado de EN-0201 durante ejecución del plan, sincronizar:
  - `docs/spec/roadmap.md`
  - `docs/spec/dependency-graph.yaml`

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de suites de integración con DB del `backend` se ejecutan sin dependencias externas adicionales.
- **SC-002**: En ejecuciones repetidas (local y CI), al menos 95% de resultados de pruebas de integración con DB se mantienen consistentes sin flaky behavior atribuible a estado compartido.
- **SC-003**: El 100% de pruebas clasificadas como integración con DB inicializan esquema de forma determinista antes de su ejecución.
- **SC-004**: El 100% de casos de integración con DB ejecutados en la suite validan aislamiento sin dependencia de estado residual entre pruebas.
- **SC-005**: El 100% de ejecuciones de runtime normal quedan fuera del baseline de DB en memoria de testing (sin activación accidental).
