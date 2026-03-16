<!--
Sync Impact Report
- Version change: 1.2.0 -> 2.0.0
- Modified principles:
  - I. Arquitectura hexagonal y limites de capas -> I. Autoridad normativa y fuente unica de verdad
  - II. Contratos explicitos, versionados y testeables -> II. Arquitectura hexagonal y separacion de modelos
  - III. Determinismo financiero y disciplina temporal -> III. Modelo economico ledger e invariantes contables
  - IV. Modelo de errores tipificados y observabilidad estructurada -> IV. Representacion determinista de dinero, porcentajes y tiempo
  - V. Atomicidad, idempotencia y concurrencia explicita -> V. Contratos externos y evolucion compatible
  - VI. Calidad verificable, TDD y gobernanza de cambios -> VI. Operacion, observabilidad e infraestructura minima viable
- Added sections:
  - Reglas Normativas del Sistema
  - Gobernanza y Enmiendas
- Removed sections:
  - Invariantes transversales
  - Restricciones operativas permanentes
  - ADR Gap
  - Estado de conflictos de fuentes autoritativas
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
  - ✅ .specify/templates/commands/*.md (directorio no existe; no aplica)
- Follow-up TODOs:
  - None
-->

# Baku Casa Constitution

## Core Principles

### I. Autoridad normativa y fuente unica de verdad
Esta constitucion define reglas invariantes del sistema y es la maxima autoridad
normativa. Cada regla del sistema MUST definirse en un unico documento y las reglas
globales MUST definirse unicamente aqui. Las especificaciones funcionales NO DEBEN
redefinir reglas ya definidas en esta constitucion; DEBEN referenciarlas. La duplicacion
de reglas en multiples documentos esta prohibida.

Rationale: mantener una jerarquia normativa unica evita contradicciones y deriva del
sistema.

### II. Arquitectura hexagonal y separacion de modelos
El backend MUST seguir arquitectura hexagonal con capas permitidas: domain,
application, interfaces e infrastructure. El dominio NO DEBE depender de
infraestructura. La capa de aplicacion MUST coordinar casos de uso, interfaces MUST
exponer adaptadores externos e infrastructure MUST implementar dependencias tecnicas. El
sistema MUST separar modelos de dominio, persistencia y API/integracion. Las conversiones
entre capas MUST ser explicitas y los contratos externos NO DEBEN exponer modelos de
persistencia.

Rationale: separar responsabilidades reduce acoplamiento y preserva mantenibilidad.

### III. Modelo economico ledger e invariantes contables
El sistema implementa un modelo contable basado en ledger append-only. Los eventos
economicos NO DEBEN eliminarse ni editarse y las correcciones MUST realizarse mediante
reversiones que crean nuevos eventos. Los importes NO DEBEN ser negativos; el signo
economico MUST derivarse del tipo de evento; las compensaciones MUST conservar el valor
total y MUST ser exactas.

Rationale: la inmutabilidad del ledger y las invariantes contables sostienen trazabilidad
y consistencia economica.

### IV. Representacion determinista de dinero, porcentajes y tiempo
Los importes monetarios MUST representarse con valores decimales exactos y esta
PROHIBIDO utilizar floats para dinero. Los porcentajes MUST representarse en rango 0-100
con precision decimal; 0 representa 0% y 100 representa 100%; tambien esta PROHIBIDO
usar floats para porcentajes. Todas las fechas y horas MUST almacenarse en UTC, las
conversiones de zona horaria MUST hacerse en presentacion y las representaciones externas
MUST ser inequivocas.

Rationale: determinismo numerico y temporal evita errores acumulativos y ambiguedades.

### V. Contratos externos y evolucion compatible
El sistema MUST exponer contratos HTTP consistentes, versionables y orientados a
recursos. Los recursos MUST representarse mediante contratos HTTP explicitos; las
operaciones MUST mapearse a semanticas HTTP estandar cuando aplique; los contratos
externos MUST ser validables y documentables. La version mayor de API MUST aparecer en
la ruta base (por ejemplo, /api/v1). Los cambios incompatibles MUST incrementar la
version mayor y los cambios compatibles MUST ser retrocompatibles. Los endpoints que
devuelven colecciones MUST estar paginados y esta PROHIBIDO devolver listas no acotadas.

Rationale: contratos estables y versionados permiten evolucion sin romper consumidores.

### VI. Operacion, observabilidad e infraestructura minima viable
El sistema MUST generar trazabilidad operativa suficiente para diagnostico y auditoria.
Los eventos operativos relevantes MUST registrarse de forma estructurada, las operaciones
correlacionables MUST incluir identificadores de correlacion y los fallos NO DEBEN
perderse de forma silenciosa. El sistema MUST poder ejecutarse en entornos domesticos o
VPS ligeros, NO DEBE depender obligatoriamente de servicios externos para funcionamiento
basico y el despliegue MUST seguir siendo viable con recursos limitados. Toda entidad
persistida MUST soportar auditoria con campos created_at, created_by, updated_at,
updated_by, deleted_at y deleted_by. Las entidades NO DEBEN eliminarse fisicamente; el
sistema MUST usar soft delete y los registros eliminados NO DEBEN aparecer en consultas
normales.

Rationale: operacion confiable y auditable es requisito de sostenibilidad del sistema.

## Reglas Normativas del Sistema

Las palabras DEBE, NO DEBE, DEBERIA y PUEDE se interpretan segun RFC 2119.

Esta constitucion regula arquitectura, modelo economico, representacion de datos,
contratos externos, operaciones, observabilidad, restricciones estructurales y gobernanza
del sistema.

La constitucion NO define comportamiento funcional. El comportamiento funcional se define
exclusivamente en docs/specs/features/* y docs/specs/enablers/*.

La constitucion NO define decisiones tecnologicas concretas. Esas decisiones DEBEN
documentarse mediante ADR en docs/decisions/adr/*.

El sistema se define mediante estas fuentes de verdad:
- docs/system/constitution.md
- docs/decisions/adr/*
- docs/planning/dependency-graph.yaml
- docs/specs/*

En caso de conflicto aplica esta precedencia:
- Constitution > ADR > Specification > Implementation

Las especificaciones NO DEBEN duplicar reglas definidas en esta constitucion.

Los mecanismos de persistencia DEBEN proporcionar estrategias de indexacion adecuadas para
consultas frecuentes y restricciones criticas.

Los Enablers introducen capacidades tecnicas reutilizables. Los Enablers marcados como
affects_future_features: true en el dependency graph forman parte del baseline tecnico
del sistema. Las Features futuras DEBEN asumir ese baseline y NO deben redefinir esas
capacidades.

Las especificaciones deben ser deterministas, evitar ambiguedad y evitar comportamiento
implicito. Si una regla puede interpretarse de multiples formas, la especificacion DEBE
aclararla explicitamente.

El desarrollo DEBE seguir Specification Driven Development (SDD): las capacidades se
introducen mediante Features y Enablers, y las implementaciones DEBEN seguir las
especificaciones.

## Gobernanza y Enmiendas

Esta constitucion prevalece sobre normas operativas de menor rango.

Las modificaciones que rompan reglas de esta constitucion DEBEN actualizar esta
constitucion.

Las modificaciones incompatibles DEBEN documentarse mediante ADR.

Toda enmienda MUST incluir justificacion, impacto, estrategia de migracion y plan de
adopcion.

Versionado de la constitucion:
- MAJOR: eliminacion o redefinicion incompatible de principios o garantias.
- MINOR: adicion de principios o ampliacion material de obligaciones normativas.
- PATCH: aclaraciones editoriales sin cambio semantico.

Revision de cumplimiento:
- Todo plan MUST pasar Constitution Check antes de diseno detallado.
- Todo PR MUST declarar impactos en contratos, invariantes, especificaciones y ADR.
- Los incumplimientos MUST bloquear merge salvo excepcion aprobada y registrada.
- Las revisiones periodicas MUST verificar coherencia entre constitucion, ADR y roadmap.

**Version**: 2.0.0 | **Ratified**: 2026-03-02 | **Last Amended**: 2026-03-16
