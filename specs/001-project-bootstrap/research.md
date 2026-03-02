# Research — EN-0100 Project Bootstrap

## Decision 1: Alcance mínimo de CI en PR
- Decision: La CI mínima obligatoria para EN-0100 será `lint + tipado + smoke tests` por root (`backend`, `bot`) en PR.
- Rationale: EN-0100 exige bootstrap verificable; la clarificación de sesión fija explícitamente ese alcance mínimo y ADR-0008 exige gates automáticos para merge.
- Alternatives considered:
  - Solo smoke tests por root: insuficiente para el objetivo de gobernanza técnica mínima.
  - Pipeline completo ADR-0008 en EN-0100: excede el alcance habilitador mínimo de este enabler.

## Decision 2: Frontera de alcance funcional
- Decision: EN-0100 NO introduce casos de uso de dominio, endpoints reales, persistencia funcional ni eventos.
- Rationale: El enabler es estrictamente de bootstrap según su spec autoritativa y roadmap; evita scope creep y preserva secuenciación incremental.
- Alternatives considered:
  - Incluir endpoint healthcheck o primer caso de uso: rechazado por ser funcionalidad de dominio/interfaz fuera de alcance.
  - Incluir modelos ORM/migraciones iniciales: rechazado por adelantar decisiones de features posteriores.

## Decision 3: Cumplimiento de arquitectura multi-root
- Decision: Implementar roots independientes con estructura mínima por root y sin runtime sharing entre roots.
- Rationale: ADR-0001 exige aislamiento, contratos versionados e independencia por root; ADR-0002 refuerza separación de capas.
- Alternatives considered:
  - Extraer librería compartida común: rechazado por violar aislamiento runtime entre roots.
  - Monolito único inicial: rechazado por contradecir multi-root aceptado.

## Decision 4: Contratos e integración
- Decision: EN-0100 no crea ni modifica contratos HTTP ni de eventos; se documenta explícitamente “sin cambios de contrato”.
- Rationale: El alcance no incluye endpoints ni eventos; ADR-0006/0004/0010 siguen vigentes para cambios futuros.
- Alternatives considered:
  - Definir contrato placeholder de API: rechazado por introducir superficie de contrato no requerida por el enabler.
  - Definir contrato de eventos inicial: rechazado por no existir publicación de eventos en alcance.

## Decision 5: Persistencia, eventos y profile `events`
- Decision: Sin cambios de persistencia ni migraciones; no se introducen eventos; profile `events` no requerido.
- Rationale: EN-0100 no incorpora lógica de dominio ni integración asíncrona; por tanto ADR-0003 y ADR-0010 no aplican materialmente en esta entrega.
- Alternatives considered:
  - Crear tabla/outbox vacía preventiva: rechazado por complejidad prematura sin caso de uso.
  - Activar profile `events` desde bootstrap: rechazado por no ser necesario en esta fase.
