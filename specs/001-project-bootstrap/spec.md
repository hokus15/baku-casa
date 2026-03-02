# Feature Specification: EN-0100 Project Bootstrap

**Feature Branch**: `001-project-bootstrap`  
**Created**: 2026-03-02  
**Status**: Draft  
**Input**: User description: "Genera la especificación de EN-0100"

## Clarifications

### Session 2026-03-02

- Q: ¿Cuál es el alcance mínimo obligatorio de CI para EN-0100? → A: CI mínimo = lint + tipado + smoke tests por root en PR.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Base mínima reproducible del repositorio (Priority: P1)

Como mantenedor del proyecto, quiero una base mínima de repositorio con roots independientes y documentación esencial para habilitar desarrollo SDD sin implementar todavía funcionalidad de dominio.

**Why this priority**: Sin esta base no existe entorno mínimo para planificar, implementar y validar cambios de forma consistente.

**Independent Test**: Puede validarse revisando la estructura mínima requerida y verificando que no existe lógica de dominio ni endpoints implementados.

**Acceptance Scenarios**:

1. **Given** un repositorio sin bootstrap completo, **When** se aplica EN-0100, **Then** existen roots independientes para backend y bot con su estructura mínima requerida.
2. **Given** el bootstrap aplicado, **When** se inspecciona la documentación base, **Then** existen README raíz, `docs/spec/` y `docs/adr/` listos para SDD.

---

### User Story 2 - Validación automática mínima por root (Priority: P2)

Como mantenedor del proyecto, quiero que cada PR ejecute validaciones mínimas por root (lint, tipado y smoke tests) para detectar roturas tempranas del bootstrap.

**Why this priority**: El bootstrap debe ser verificable automáticamente para sostener gobernanza y reproducibilidad.

**Independent Test**: Puede validarse comprobando que el pipeline de CI ejecuta lint, tipado y smoke tests para backend y bot en PR.

**Acceptance Scenarios**:

1. **Given** una pull request abierta, **When** se ejecuta CI, **Then** se ejecutan lint, tipado y smoke tests para backend y bot y el resultado queda reportado.

---

### User Story 3 - Aislamiento del alcance del enabler (Priority: P3)

Como responsable de arquitectura, quiero garantizar que EN-0100 no incorpora casos de uso, endpoints ni persistencia de negocio para mantener el alcance del enabler acotado.

**Why this priority**: Evita deriva de alcance y mantiene trazabilidad con roadmap y ADR.

**Independent Test**: Puede validarse comprobando ausencia de artefactos funcionales de dominio y de contratos API reales en esta entrega.

**Acceptance Scenarios**:

1. **Given** la implementación de EN-0100, **When** se revisa el contenido entregado, **Then** solo existe bootstrap estructural y validación mínima, sin lógica de negocio ni endpoints reales.

---

### Edge Cases

- ¿Qué ocurre si existe un root requerido sin carpeta de tests mínima?
- ¿Qué ocurre si CI valida un root y omite el otro por configuración incompleta?
- ¿Qué ocurre si CI ejecuta tests pero omite lint o tipado en alguno de los roots?
- ¿Qué ocurre si se añade accidentalmente lógica de dominio o endpoints durante el bootstrap?
- ¿Qué ocurre si un root cumple estructura pero no puede ejecutar su smoke test?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST disponer de roots independientes para backend y bot como base inicial del monorepo multi-root.
- **FR-002**: Cada root inicial MUST incluir, como mínimo, archivo de proyecto, código fuente y carpeta de pruebas.
- **FR-003**: El repositorio MUST incluir documentación base de especificaciones y decisiones arquitectónicas.
- **FR-004**: El repositorio MUST incluir README raíz con descripción funcional y validaciones básicas de arranque.
- **FR-005**: El sistema MUST ejecutar validaciones mínimas por root en cada PR mediante pipeline de CI: lint, tipado y smoke tests.
- **FR-006**: Debe existir al menos una prueba smoke por root para verificar ejecución del runner de tests.
- **FR-007**: El enabler MUST evitar introducir casos de uso de dominio, endpoints reales o persistencia funcional.
- **FR-008**: El bootstrap MUST preservar aislamiento entre roots y PROHIBITED acoplamiento runtime entre ellos.
- **FR-009**: EN-0100 MUST NOT introducir contratos funcionales nuevos; si aparecen en evolución posterior, MUST respetar versionado y compatibilidad definidos por ADR.
- **FR-010**: La entrega MUST ser coherente con disciplina SDD: especificación vigente, trazabilidad y cumplimiento de gobernanza de CI.

### Non-Functional Requirements

- **NFR-001**: La validación mínima en PR MUST ser reproducible y determinista entre ejecuciones equivalentes.
- **NFR-002**: El bootstrap MUST poder ejecutarse en entorno self-hosted de recursos limitados sin requerir servicios externos obligatorios.
- **NFR-003**: Los checks mínimos MUST fallar explícitamente cuando falte estructura base o cuando un root no cumpla lint, tipado o smoke tests.
- **NFR-004**: El alcance del enabler MUST permanecer acotado a preparación estructural e infraestructura mínima de validación.

### Constitution Alignment *(mandatory)*

- **CA-001**: Impacto de capas: sin cambio de reglas de dominio; se habilita solo base estructural para respetar límites arquitectura.
- **CA-002**: Impacto de contratos: no se define contrato funcional nuevo; se mantiene disciplina de contratos versionados para integraciones futuras.
- **CA-003**: Contract tests: se exige capacidad de test por root y compatibilidad en CI cuando existan cambios de contrato.
- **CA-004**: Invariantes financieros/temporales: sin cambio funcional en dinero, porcentajes o tiempo; se preserva cumplimiento constitucional para trabajo posterior.
- **CA-005**: Impacto documental: este enabler actualiza especificación; no introduce cambio estructural adicional fuera de ADR aceptados.

### Key Entities *(include if feature involves data)*

- **Root Independiente**: Unidad aislada del monorepo con ciclo de validación propio.
- **Estructura Mínima de Root**: Conjunto mínimo de artefactos requeridos para desarrollar y probar cada root.
- **Pipeline de CI de PR**: Mecanismo de validación automática que ejecuta pruebas mínimas por root en cada pull request.
- **Smoke Test de Root**: Prueba mínima para verificar que el runner de tests del root funciona.

## Assumptions

- El alcance de EN-0100 es exclusivamente habilitador y previo a features de dominio.
- El sistema mantiene modelo self-hosted y no requiere exposición pública por defecto.
- El bootstrap se limita a backend y bot, permitiendo ampliación futura a nuevos roots.
- La gobernanza de merge permanece condicionada a CI en verde.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los roots iniciales definidos (backend y bot) cumple estructura mínima verificable en revisión.
- **SC-002**: El 100% de PRs que tocan bootstrap ejecuta lint, tipado y smoke tests por root en CI.
- **SC-003**: El 100% de roots iniciales dispone de smoke test ejecutable en CI.
- **SC-004**: Cero artefactos de dominio funcional, endpoints reales o persistencia de negocio introducidos en EN-0100.
