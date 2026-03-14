Source (fuente de verdad de la funcionalidad):

docs/specs/features/{{FEATURE_FILE}}.md
ocs/specs/enabler/{{ENABLER_FILE}}.md

Reglas del sistema:

docs/system/constitution.md

Contexto del sistema:

docs/system/context.md  
docs/system/glossary.md

Gobernanza de documentación:

docs/meta/doc-governance.md

Definiciones reutilizables (si aplican):

docs/specs/shared/

Dependencias estructurales:

docs/planning/dependency-graph.yaml

Reglas:

- La especificación debe basarse exclusivamente en la feature indicada.
- No inventes comportamiento no definido en la feature.
- Respeta todas las reglas definidas en `docs/system/constitution.md`.
- Si una definición ya existe en `docs/specs/shared/`, reutilízala y no la dupliques.
- No inventes dependencias; usa únicamente `docs/planning/dependency-graph.yaml`.
- Si la feature es ambigua o incompleta, solicita aclaración antes de generar la spec.
- No introduzcas decisiones técnicas ni detalles de implementación.
- Describe únicamente comportamiento funcional del dominio.
- Mantén consistencia con la terminología definida en `docs/system/glossary.md`.
- Mantén consistencia con el contexto definido en `docs/system/context.md`.
