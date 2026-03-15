# Spec-Kit Prompt Template — `/speckit.plan`

Crea el plan técnico de implementación de un Roadmap Item usando el stack tecnológico elegido por el proyecto.

El item puede ser:

- una Feature
- un Enabler

El objetivo es definir cómo implementar la especificación del item de forma consistente con la arquitectura, las decisiones técnicas y el baseline ya existente del sistema.

## Entrada principal

Usa como documento principal la especificación vigente del item:

- `docs/specs/features/<feature-file>.md`, o
- `docs/specs/enablers/<enabler-file>.md`

## Contexto mínimo permitido

Resuelve primero el contexto mínimo del item con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase plan --profile default`

La salida de esa utilidad es la entrada base obligatoria de esta fase.

Usa como contexto mínimo exactamente los artefactos devueltos por esa utilidad para el item y la fase actual.

Solo amplía el contexto si los artefactos resueltos no bastan para producir un plan técnico fiable.

Debes tratar el bloque `Core technical baseline` devuelto por la utilidad como el stack y baseline técnico efectivos del item para esta fase. Usa `Supporting technical baseline` y `Supporting ADRs` solo cuando el plan necesite más detalle o una integración adicional.

Prioriza primero `Direct dependencies` para integrar el item con su baseline inmediato. Usa `Transitive baseline dependencies` solo cuando el plan necesite confirmar capacidades heredadas más lejanas del DAG.

Interpreta `Direct shared specs` como contratos compartidos que el plan debe respetar de forma explícita. Usa `Inherited shared specs` solo cuando el plan necesite reusar semántica ya introducida por dependencias.

Interpreta `Core constitution sections` y `Core context sections` como el baseline normativo y operativo explícito del item. Usa `Supporting constitution sections` y `Supporting context sections` solo cuando el plan necesite baseline adicional aportado por los slices.

En esta fase, si necesitas profundizar manualmente, usa `reason` para decidir qué ADRs cargar en detalle y prioriza los de impacto técnico material.

No cargues por defecto el resto de `docs/`.

## Qué debe cubrir el plan

- estrategia de implementación del item
- descomposición técnica del trabajo
- capas o áreas del sistema afectadas
- integración con el baseline existente
- contratos, persistencia, eventos, configuración y observabilidad cuando apliquen
- validaciones, pruebas y riesgos técnicos relevantes
- actualizaciones documentales necesarias para mantener consistencia

## Reglas

- Basa el plan exclusivamente en la especificación del item y en las fuentes autoritativas mínimas necesarias para convertirla en un plan técnico viable.
- Usa el stack tecnológico ya adoptado por el proyecto; no introduzcas tecnologías nuevas salvo que una fuente autoritativa vigente las respalde o el análisis evidencie un hueco que requiera ADR.
- No inventes comportamiento funcional que no esté definido, implícito de forma razonable o exigido por una regla global aplicable.
- No introduzcas dependencias no respaldadas por `docs/planning/dependency-graph.yaml`.
- No redefinas reglas globales ya definidas en `docs/system/constitution.md`; el plan debe respetarlas.
- Mantén consistencia con la terminología de `docs/system/glossary.md` cuando aplique.
- Mantén consistencia con el contexto operativo definido en `docs/system/context.md`.
- Mantén consistencia con ADRs relevantes y explica su impacto solo cuando sea material para la implementación.

## Dependencias y baseline

- Analiza `docs/planning/dependency-graph.yaml` antes de planificar el item.
- El plan debe respetar el orden de ejecución definido por el DAG.
- Si el item es una Feature, debe asumirse como baseline toda capacidad previa aplicable propagada por el grafo.
- El plan no debe ignorar Enablers ya aplicables ni duplicar capacidades técnicas ya introducidas.
- Si el item es un Enabler, debes tener en cuenta el impacto del plan sobre Features existentes que dependan de él, directa o transitivamente, siempre que ya estén documentadas.
- No anticipes cambios en Features o Enablers aún no definidos documentalmente.

## Impacto técnico

- Identifica las áreas técnicas materialmente afectadas por la implementación.
- Identifica si el item introduce o modifica contratos HTTP, persistencia, eventos, configuración, observabilidad, seguridad, tareas programadas u otros mecanismos transversales.
- Si hay impacto contractual o de integración, el plan debe reflejar cómo se preserva la compatibilidad o qué cambio documental debe registrarse.
- Si el item requiere una decisión arquitectónica no cubierta por la documentación vigente, márcalo explícitamente como hueco de ADR.

## Disciplina de documentación

- La documentación debe quedar actualizada y consistente como parte del plan.
- Si el plan revela una regla global nueva o una modificación de una existente, debe actualizarse `docs/system/constitution.md`.
- Si el plan revela una restricción operativa, hecho del sistema o contexto global nuevo o modificado, debe actualizarse `docs/system/context.md`.
- Si el plan introduce o aclara terminología compartida relevante, debe actualizarse `docs/system/glossary.md`.
- Si el plan cambia dependencias, baseline, propagación estructural o estado del roadmap, deben actualizarse `docs/planning/dependency-graph.yaml` y `docs/planning/roadmap.md` cuando aplique.
- Si el plan cambia el contexto mínimo, referencias normativas o slices documentales aplicables, deben actualizarse los artefactos de planificación correspondientes, incluyendo `docs/planning/item-manifest.yaml`, `docs/planning/context-slices.yaml` y `docs/planning/adr-map.yaml` cuando aplique.
- Si el plan evidencia una decisión técnica nueva o una modificación material de una existente, debe crearse o actualizarse el ADR correspondiente.
- Si la especificación o la documentación existente entran en conflicto con el plan derivado de fuentes autoritativas, el conflicto debe corregirse y no ignorarse.
- Las actualizaciones documentales deben limitarse a los artefactos materialmente afectados; no debe reescribirse documentación no relacionada.
- Debe ejecutarse `python tools/lint_sdd.py` al final de la fase para validar que la documentación resultante sigue siendo consistente.
- La fase no debe cerrarse si el linter documental falla.

## Restricciones de contenido

- No incluyas código.
- No conviertas el plan en una reescritura de la especificación funcional.
- No uses rutas absolutas.
- No describas tareas irrelevantes para el item.
- No introduzcas decisiones arquitectónicas que contradigan ADRs vigentes.
- No inventes detalles de implementación que no puedan justificarse con la especificación o el baseline del proyecto.

## Manejo de bloqueos

- Si existen ambigüedades o contradicciones que impidan un plan fiable, márcalas explícitamente como pendientes de aclarar.
- No resuelvas bloqueos inventando comportamiento o decisiones técnicas no respaldadas.
- Los pendientes deben quedar formulados de manera concreta y accionable para que puedan resolverse antes de la implementación.
