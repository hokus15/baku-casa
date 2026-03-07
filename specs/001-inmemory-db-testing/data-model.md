# Data Model: EN-0201 In-Memory Database Testing Baseline

## Overview
EN-0201 no introduce entidades de dominio ni cambios en el modelo funcional del negocio.
No se define un data model de negocio para este enabler.

## Configuration Artifact (Non-Domain)

### Testing DB Connection Context
- Purpose: Definir el contexto de conexión para pruebas con persistencia en memoria.
- Scope: Exclusivo para entorno de testing.
- Constraints:
  - Activación explícita.
  - Separado de runtime normal.
  - Sin ambigüedad con configuraciones persistentes.

## Lifecycle Rules

- Inicialización de esquema determinista para pruebas de integración.
- Aislamiento de estado entre tests.
- Reproducibilidad equivalente local/CI.

## Validation Rules
- El contexto de conexión de testing en memoria debe ser explícito y no ambiguo.
- Las pruebas de integración con DB deben ejecutarse sin dependencia de estado compartido entre casos.
- El esquema de pruebas debe inicializarse de manera determinista.
- El baseline no debe modificar comportamiento de runtime fuera del contexto de testing.

## Notes
- Este artefacto existe para documentar que el impacto es de configuración y ciclo de ejecución de pruebas, no de modelo de dominio.
- No hay impacto en contratos externos ni versionado de API/eventos.
