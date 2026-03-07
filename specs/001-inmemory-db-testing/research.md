# Research: EN-0201 In-Memory Database Testing Baseline

## Decision 1: Configuración de testing explícita y separada
- Decision: Definir y activar de forma explícita un perfil/configuración de testing aislado del runtime normal para pruebas con DB en memoria.
- Rationale: Alinea con ADR-0013 (configuración centralizada y validada) y evita ejecuciones accidentales contra entornos persistentes.
- Alternatives considered:
  - Reutilizar configuración de desarrollo: rechazada por ambigüedad operativa.
  - Inferir modo testing implícitamente: rechazado por baja seguridad y reproducibilidad.

## Decision 2: Inicialización determinista del esquema en pruebas
- Decision: Establecer una política determinista para disponer del esquema de persistencia al inicio de pruebas de integración con DB.
- Rationale: Cumple EN-0201 y ADR-0003, reduciendo drift y resultados no reproducibles.
- Alternatives considered:
  - Inicialización ad-hoc por caso sin política común: rechazada por inconsistencia.
  - Dependencia de estado previo de ejecución: rechazada por romper aislamiento.

## Decision 3: Aislamiento fuerte entre tests con DB
- Decision: Definir una estrategia uniforme para garantizar independencia de estado entre pruebas de integración con persistencia.
- Rationale: Evita acoplamiento temporal entre pruebas y flaky behavior en local/CI.
- Alternatives considered:
  - Limpieza manual no estandarizada: rechazada por fragilidad.
  - Compartir estado persistente entre tests: rechazado por violar criterios de aceptación de EN-0201.

## Decision 4: Convenciones de clasificación y ubicación de pruebas
- Decision: Establecer convenciones para identificar pruebas unitarias vs integración con DB y su ubicación dentro de `backend/tests/`.
- Rationale: Mejora trazabilidad, ejecución selectiva y gobernanza de calidad (ADR-0008).
- Alternatives considered:
  - Sin clasificación explícita: rechazada por pérdida de claridad operativa.

## Decision 5: Sin cambios contractuales externos
- Decision: Tratar EN-0201 como enabler interno sin impacto en contratos HTTP/eventos.
- Rationale: El objetivo es baseline de testing, no superficie de integración.
- Alternatives considered:
  - Exponer capacidades de testing por API/eventos: fuera de alcance del roadmap.

## Decision 6: Compatibilidad local/CI sin dependencias externas
- Decision: El baseline debe ser ejecutable de forma consistente en entorno local y en CI sin servicios adicionales.
- Rationale: Alineado con ADR-0008 y con el contexto self-hosted de baja complejidad operativa.
- Alternatives considered:
  - Requerir servicios de infraestructura para pruebas: rechazado por aumentar fricción y complejidad.
