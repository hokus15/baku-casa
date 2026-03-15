# Spec-Kit Prompt Template — `/speckit.analyze`

Realiza un análisis transversal de consistencia y cobertura entre los artefactos del Roadmap Item antes de continuar con `speckit.implement`.

Este análisis debe ejecutarse después de `speckit.tasks` y antes de `speckit.implement`.

El item puede ser:

- una Feature
- un Enabler

El objetivo es verificar que la cadena documental y de planificación del item sea internamente consistente, suficientemente completa y alineada con las fuentes de verdad del sistema.

## Entradas principales

Usa como entradas principales todos los artefactos vigentes del item que ya deberían existir en este punto del flujo:

- la especificación vigente del item
- los resultados de clarificación del item, si existen
- el plan técnico vigente del item
- la lista de tareas vigente del item

## Contexto mínimo permitido

Resuelve primero el contexto mínimo del item con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase analyze --profile default`

La salida de esa utilidad es la entrada base obligatoria de esta fase.

Usa como contexto mínimo exactamente los artefactos devueltos por esa utilidad para el item y la fase actual, junto con los artefactos ya producidos del item.

Solo amplía el contexto si los artefactos resueltos no bastan para evaluar consistencia o cobertura.

Debes usar el bloque `Core technical baseline` devuelto por la utilidad para verificar que plan y tareas no se desvían del stack y baseline aplicables al item. Usa `Supporting technical baseline` y `Supporting ADRs` solo cuando el análisis de riesgo o cobertura requiera más detalle.

Prioriza primero `Direct dependencies` al comprobar consistencia del baseline inmediato. Usa `Transitive baseline dependencies` solo cuando el riesgo o la cobertura analizada dependan de capacidades heredadas más alejadas.

Interpreta `Direct shared specs` como contratos compartidos exigibles directamente al item. Usa `Inherited shared specs` solo cuando el análisis deba comprobar alineación con semántica heredada por dependencias.

Interpreta `Core constitution sections` y `Core context sections` como el baseline normativo y operativo directo del item. Usa `Supporting constitution sections` y `Supporting context sections` solo cuando el análisis de cobertura o riesgo necesite baseline adicional aportado por los slices.

En esta fase, si necesitas profundizar manualmente, usa `reason` para priorizar ADRs relacionados con el tipo de riesgo analizado.

No cargues por defecto el resto de `docs/`.

## Qué debe analizarse

- consistencia entre especificación, clarificación, plan y tareas
- cobertura de requisitos y reglas del item a través de plan y tareas
- alineación con constitución, contexto, ADRs, DAG y baseline
- huecos entre lo especificado y lo planificado
- huecos entre lo planificado y lo descompuesto en tareas
- contradicciones internas o externas entre artefactos
- ausencia de trabajo documental necesario
- bloqueos que deban resolverse antes de implementar

## Reglas

- Basa el análisis exclusivamente en los artefactos vigentes del item y en las fuentes autoritativas mínimas necesarias para evaluar consistencia y cobertura.
- No inventes requisitos, comportamiento ni trabajo técnico que no esté respaldado por los artefactos existentes o por reglas globales aplicables.
- No introduzcas dependencias no respaldadas por `docs/planning/dependency-graph.yaml`.
- No redefinas reglas globales ya definidas en `docs/system/constitution.md`; el análisis debe comprobar su cumplimiento.
- Mantén consistencia con la terminología de `docs/system/glossary.md` cuando aplique.
- Mantén consistencia con ADRs relevantes sin reescribir su contenido.

## Dependencias y baseline

- Analiza `docs/planning/dependency-graph.yaml` antes de emitir el análisis.
- Verifica que spec, plan y tareas respeten el orden de ejecución definido por el DAG.
- Si el item es una Feature, verifica que todos los Enablers previos aplicables del baseline estén asumidos correctamente y no se estén duplicando capacidades técnicas ya existentes.
- Si el item es un Enabler, verifica que su impacto sobre Features existentes documentadas esté reflejado de manera consistente en los artefactos que corresponda.
- No anticipes cambios en Features o Enablers aún no definidos documentalmente.

## Cobertura mínima que debe validarse

- todas las reglas e invariantes materiales de la especificación tienen reflejo en el plan o en las tareas
- todos los riesgos, integraciones y áreas técnicas relevantes del plan tienen reflejo en las tareas cuando corresponda
- todas las dependencias y supuestos críticos están explícitos
- todas las actualizaciones documentales necesarias están recogidas
- no quedan ambigüedades críticas sin marcar que puedan comprometer `speckit.implement`

## Disciplina de documentación

- El análisis debe comprobar que la documentación vaya a quedar actualizada y consistente.
- Si detecta que faltan actualizaciones en `docs/system/constitution.md`, `docs/system/context.md`, `docs/system/glossary.md`, `docs/planning/dependency-graph.yaml`, `docs/planning/roadmap.md`, `docs/planning/item-manifest.yaml`, `docs/planning/context-slices.yaml` o `docs/planning/adr-map.yaml`, debe marcar ese hueco explícitamente.
- Si detecta que falta crear o actualizar un ADR, debe marcarlo explícitamente.
- Si detecta contradicciones entre artefactos, debe indicar qué fuente de verdad prevalece y qué documento debe corregirse.
- No debe asumirse que la documentación vigente es correcta si el análisis demuestra que está desalineada.

## Restricciones de contenido

- No propongas implementación detallada ni código.
- No conviertas el análisis en una reescritura de la especificación, del plan o de las tareas.
- No introduzcas decisiones arquitectónicas nuevas.
- No modifiques ADR existentes desde el propio análisis.
- No introduzcas tecnologías no respaldadas por la documentación vigente.

## Manejo de hallazgos y bloqueos

- Si detectas inconsistencias, huecos de cobertura o contradicciones, márcalos explícitamente como hallazgos a resolver antes de `speckit.implement`.
- Si existen ambigüedades o dependencias no resueltas que comprometan la implementación, márcalas como pendientes de aclarar.
- No resuelvas bloqueos inventando comportamiento o decisiones técnicas no respaldadas.
- Los hallazgos y pendientes deben quedar formulados de manera concreta, accionable y trazable al artefacto afectado.
