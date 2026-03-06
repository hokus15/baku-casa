<!--
Sync Impact Report
- Version change: 1.1.0 -> 1.1.1
- Modified principles:
	- None
- Added sections:
	- None
- Removed sections:
	- Conflictos de fuentes autoritativas detectados (reemplazada por estado de validación)
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md
	- ✅ .specify/templates/spec-template.md
	- ✅ .specify/templates/tasks-template.md (sin cambios; validado alineado)
	- ✅ .specify/templates/commands/*.md (no existe directorio; no aplica)
- Follow-up TODOs:
	- None
-->

# Baku Casa Constitution

## Core Principles

### I. Arquitectura hexagonal y límites de capas
El sistema MUST mantener separación estricta entre Domain, Application, Interfaces e
Infrastructure. Domain MUST permanecer libre de dependencias de framework, IO,
persistencia y transporte. La lógica de negocio fuera de Domain/Application está
PROHIBITED. El mapeo Domain <-> ORM y Domain <-> API MUST ser explícito.

Rationale: evita acoplamiento accidental y preserva testabilidad aislada del núcleo.

### II. Contratos explícitos, versionados y testeables
Toda integración entre roots o componentes aislados MUST ocurrir exclusivamente mediante
contratos explícitos y versionados (HTTP y/o eventos). El acoplamiento runtime directo y
los imports cruzados entre roots están PROHIBITED. Cambios incompatibles MUST incrementar
MAJOR. Dentro de una misma MAJOR, eliminar/renombrar campos o cambiar semántica está
PROHIBITED. Todo cambio de contrato MUST incluir contract tests en CI.

Rationale: preserva compatibilidad evolutiva y evita romper consumidores de forma tácita.

### III. Determinismo financiero y disciplina temporal
Dinero y porcentajes MUST usar Decimal; float está PROHIBITED en lógica de dominio y
persistencia semántica. Los porcentajes MUST representarse en rango 0-100 en todas las
capas; el modelo 0-1 persistente/de dominio está PROHIBITED. El redondeo financiero MUST
ser explícito y determinista. El tiempo interno MUST ser UTC, timezone-aware, y
serializado en ISO 8601/RFC3339. datetime naive está PROHIBITED.

Rationale: evita deriva numérica/temporal y garantiza consistencia contable verificable.

### IV. Modelo de errores tipificados y observabilidad estructurada
Los errores de negocio/aplicación MUST estar tipificados con código estable en inglés y
mapeo determinista a contratos externos. Exponer detalles internos de excepción está
PROHIBITED. Las respuestas de error MUST incluir error_code, message y correlation_id.
Todo log técnico MUST ser estructurado, en inglés y con timestamp UTC.

Rationale: estabiliza el contrato de error y mejora diagnóstico operativo sin filtrar
detalles internos.

### V. Atomicidad, idempotencia y concurrencia explícita
Toda operación económica que cambie estado MUST ejecutarse en transacción atómica con
rollback completo ante fallo. Las operaciones con efecto económico MUST ser idempotentes y
proteger duplicados mediante clave/id único persistido o mecanismo equivalente. El patrón
last-write-wins en flujos contables está PROHIBITED. El conflicto de concurrencia MUST
fallar de forma explícita con error tipificado.

Rationale: protege invariantes contables frente a reintentos, concurrencia y fallos.

### VI. Calidad verificable, TDD y gobernanza de cambios
Todo cambio funcional MUST seguir ciclo TDD (red -> green -> refactor) con evidencia en
tests. Ningún merge está permitido sin CI en verde (lint, type-check, unit, integration,
contract cuando aplique). Todo cambio de comportamiento MUST actualizar spec en el mismo
change set. Todo cambio estructural/arquitectónico MUST actualizar o crear ADR.
Excepciones temporales MUST ser explícitas, justificadas y con fecha de retiro.

Rationale: reduce regresiones y mantiene trazabilidad entre intención, diseño y entrega.

## Invariantes transversales

- El ledger económico es append-only: modificación/borrado lógico de eventos económicos
	está PROHIBITED.
- Las correcciones económicas MUST realizarse mediante eventos compensatorios trazables.
- La conservación de valor y el cuadrado exacto de allocations MUST mantenerse.
- correlation_id MUST propagarse en entrada, procesamiento e integración saliente.
- IDs persistentes MUST ser opacos, estables e inmutables; semántica embebida en IDs está
	PROHIBITED.
- Todo conjunto cerrado relevante MUST modelarse como enumeración centralizada.
- DRY MUST aplicarse dentro de un contexto; duplicación intencional entre roots MAY
	aceptarse para preservar aislamiento.

## Restricciones operativas permanentes

- El despliegue MUST ser reproducible, autocontenido y compatible con modelo self-hosted.
- La exposición a internet por defecto está PROHIBITED; el modo por defecto MUST minimizar
	superficie pública.
- El sistema MUST soportar backup y restore verificables del estado persistente.
- Las migraciones MUST preservar restaurabilidad, integridad y trazabilidad de datos.
- Cambios destructivos sin estrategia explícita de preservación y verificación están
	PROHIBITED.
- La configuración de runtime MUST ser tipada, centralizada y validada en arranque.

## ADR Gap

- Regla constitucional sin ADR dedicado: TDD obligatorio (red -> green -> refactor) como
	requisito de proceso verificable. Actualmente existe cobertura parcial en ADR-0008
	(gates de CI), pero no una decisión arquitectónica explícita sobre disciplina TDD.
	Recomendación: registrar ADR específico de test strategy/process governance.

## Estado de conflictos de fuentes autoritativas

- No se detectan conflictos activos en las fuentes autoritativas validadas para esta
  enmienda.
- Se verificó la alineación de IDs de enablers (`EN-0200`, `EN-0201`, `EN-0202`) entre:
  `docs/spec/roadmap.md`, `docs/spec/dependency-graph.yaml` y
  `docs/spec/enablers-taxonomy.md`.

## Governance

- Esta constitución prevalece sobre normas operativas de menor rango.
- Toda enmienda MUST incluir: justificación, impacto, estrategia de migración y plan de
	adopción.
- Versionado de la constitución:
	- MAJOR: eliminación/redefinición incompatible de principios o garantías.
	- MINOR: adición de principios o ampliación material de obligaciones normativas.
	- PATCH: aclaraciones editoriales sin cambio semántico.
- Revisión de cumplimiento:
	- Todo plan MUST pasar Constitution Check antes de diseño detallado.
	- Todo PR MUST declarar impactos en contratos, invariantes, spec y ADR.
	- Incumplimientos MUST bloquear merge salvo excepción aprobada y registrada.
	- Revisiones periódicas MUST verificar coherencia entre constitución, ADR y roadmap.

**Version**: 1.1.1 | **Ratified**: 2026-03-02 | **Last Amended**: 2026-03-06
