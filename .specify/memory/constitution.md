<!--
Sync Impact Report
- Version change: unversioned-template → 1.0.0
- Modified principles:
	- Template Principle 1 → I. Separación de capas y límites arquitectónicos
	- Template Principle 2 → II. Disciplina de contratos y versionado
	- Template Principle 3 → III. Errores tipificados y semántica estable
	- Template Principle 4 → IV. Determinismo financiero y consistencia temporal
	- Template Principle 5 → V. Verificación, CI y documentación viva
- Added sections:
	- Invariantes transversales
	- Restricciones operativas permanentes
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md
	- ✅ .specify/templates/spec-template.md
	- ✅ .specify/templates/tasks-template.md
	- ✅ .specify/templates/commands/*.md (no files present)
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): No se encontró la fecha original de ratificación en el contexto disponible.
-->

# Baku Casa Constitution

## Core Principles

### I. Separación de capas y límites arquitectónicos
El sistema SHALL mantener separación estricta entre dominio, aplicación, interfaces e
infraestructura. El dominio MUST permanecer libre de dependencias de transporte,
persistencia y framework. La lógica de negocio fuera del dominio y aplicación está
PROHIBITED. El mapeo entre modelos internos y contratos externos MUST ser explícito.

### II. Disciplina de contratos y versionado
Toda integración entre componentes aislados SHALL realizarse por contratos explícitos y
versionados. El acoplamiento runtime directo entre componentes aislados está PROHIBITED.
Un cambio incompatible MUST incrementar versión MAJOR. Dentro de la misma MAJOR,
eliminar/renombrar campos o alterar semántica está PROHIBITED. Todo cambio de contrato
MUST incluir contract tests de compatibilidad.

### III. Errores tipificados y semántica estable
Los errores de negocio y aplicación MUST estar tipificados y exponer códigos estables en
inglés. Exponer detalles internos de excepción está PROHIBITED. Las respuestas de error
MUST incluir código estable, mensaje legible y correlation_id. El mapeo de errores a
respuestas externas SHALL ser determinista y consistente.

### IV. Determinismo financiero y consistencia temporal
El cálculo financiero SHALL ser determinista. Para dinero y porcentajes, MUST usarse
Decimal y float está PROHIBITED. Los porcentajes MUST representarse en rango 0–100 en
todas las capas; el modelo 0–1 persistente o de dominio está PROHIBITED. El tiempo
interno MUST ser UTC con datetime timezone-aware y serialización ISO 8601/RFC3339.
datetime naive está PROHIBITED.

### V. Verificación, CI y documentación viva
Ningún cambio SHALL fusionarse sin CI en verde. Si cambia un contrato, los contract
tests MUST actualizarse y ejecutarse. Todo cambio de comportamiento MUST actualizar la
spec en el mismo change set. Todo cambio estructural o arquitectónico MUST registrarse
mediante ADR. Las excepciones temporales MUST ser explícitas, justificadas y con fecha
límite de eliminación.

## Invariantes transversales

- Las operaciones críticas de dominio MUST preservar atomicidad, idempotencia y manejo
	explícito de conflicto de concurrencia.
- El patrón last-write-wins en flujos contables está PROHIBITED.
- Los eventos económicos contables MUST ser inmutables y sus correcciones SHALL
	realizarse mediante compensaciones trazables.
- El correlation_id MUST propagarse entre entrada, procesamiento e integración saliente.
- DRY MUST aplicarse dentro de cada contexto; duplicación intencional entre componentes
	aislados MAY aceptarse para preservar límites.
- Compartir runtime entre componentes aislados está PROHIBITED.

## Restricciones operativas permanentes

- El despliegue SHALL ser reproducible y autocontenido.
- La exposición pública por defecto está PROHIBITED; la postura por defecto MUST
	minimizar superficie de exposición.
- El sistema MUST soportar backup y restore verificables del estado persistente.
- Las migraciones MUST preservar restaurabilidad e integridad.
- Cambios destructivos de datos sin estrategia de preservación/verificación están
	PROHIBITED.

## Governance

- Esta constitución prevalece sobre normas operativas de menor rango.
- Toda enmienda MUST incluir justificación, impacto de migración y plan de adopción.
- Versionado de la constitución:
	- MAJOR: eliminación o redefinición incompatible de principios.
	- MINOR: adición de principio o ampliación material de reglas obligatorias.
	- PATCH: aclaraciones no semánticas y correcciones editoriales.
- Revisión de cumplimiento:
	- Todo plan MUST pasar Constitution Check antes de implementar.
	- Todo PR MUST declarar impactos en contratos, spec y ADR.
	- El incumplimiento MUST bloquear merge salvo excepción aprobada y registrada.

**Version**: 1.0.0 | **Ratified**: 2026-03-02 | **Last Amended**: 2026-03-02
