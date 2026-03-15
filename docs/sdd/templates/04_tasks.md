# Spec-Kit Prompt Template — `/speckit.tasks`

Genera una lista de tareas accionables para implementar un Roadmap Item a partir de su plan técnico vigente.

El item puede ser:

- una Feature
- un Enabler

El objetivo es descomponer el trabajo de implementación en tareas claras, ejecutables y ordenadas, manteniendo consistencia con la especificación, el plan y el baseline del sistema.

## Entrada principal

Usa como entradas principales:

- la especificación vigente del item:
  - `docs/specs/features/<feature-file>.md`, o
  - `docs/specs/enablers/<enabler-file>.md`
- el plan técnico vigente del item generado por `speckit.plan`

## Contexto mínimo permitido

Resuelve primero el contexto mínimo del item con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase tasks --profile default`

La salida de esa utilidad es la entrada base obligatoria de esta fase.

Usa como contexto mínimo exactamente los artefactos devueltos por esa utilidad para el item y la fase actual, junto con el plan técnico vigente del item.

Solo amplía el contexto si los artefactos resueltos no bastan para descomponer trabajo accionable sin ambigüedad.

Debes tratar el bloque `Core technical baseline` devuelto por la utilidad como baseline técnico efectivo del item al derivar tareas. Usa `Supporting technical baseline` y `Supporting ADRs` solo cuando una tarea necesite profundizar en una integración o restricción adicional.

Prioriza primero `Direct dependencies` al derivar trabajo ejecutable. Usa `Transitive baseline dependencies` solo cuando una tarea dependa explícitamente de una capacidad heredada no cubierta por la dependencia directa.

Interpreta `Direct shared specs` como contratos compartidos que deben verse reflejados directamente en las tareas. Usa `Inherited shared specs` solo cuando la descomposición necesite respetar una semántica heredada por baseline.

Interpreta `Core constitution sections` y `Core context sections` como el baseline normativo y operativo directo del item. Usa `Supporting constitution sections` y `Supporting context sections` solo cuando la descomposición necesite respetar baseline adicional aportado por los slices.

En esta fase, si necesitas profundizar manualmente, usa `reason` para evitar convertir ADRs no materialmente cargados en tareas espurias.

No cargues por defecto el resto de `docs/`.

## Qué deben conseguir las tareas

- convertir el plan técnico en trabajo ejecutable
- cubrir todas las áreas necesarias para completar el item
- reflejar dependencias y orden lógico de ejecución
- incluir validación y pruebas cuando apliquen
- incluir actualización documental cuando sea necesaria
- dejar el item en un estado implementable sin ambigüedad operativa

## Reglas

- Basa las tareas exclusivamente en la especificación del item, su plan técnico y en las fuentes autoritativas mínimas necesarias para mantener consistencia.
- Las tareas deben ser concretas, accionables y suficientemente pequeñas para poder ejecutarse y verificarse.
- Ordena las tareas de forma coherente con las dependencias del item y con la secuencia técnica del plan.
- No inventes comportamiento funcional ni trabajo no respaldado por la especificación o el plan.
- No introduzcas dependencias no respaldadas por `docs/planning/dependency-graph.yaml`.
- No redefinas reglas globales ya definidas en `docs/system/constitution.md`; las tareas deben respetarlas.
- Mantén consistencia con la terminología de `docs/system/glossary.md` cuando aplique.
- Mantén consistencia con ADRs relevantes sin reescribir su contenido.

## Dependencias y baseline

- Analiza `docs/planning/dependency-graph.yaml` antes de generar las tareas.
- Las tareas deben respetar el orden de ejecución definido por el DAG.
- Si el item es una Feature, deben asumirse como baseline las capacidades previas aplicables propagadas por el grafo.
- Las tareas no deben duplicar capacidades técnicas ya introducidas por Enablers existentes.
- Si el item es un Enabler, debes tener en cuenta el impacto de su implementación sobre Features existentes que dependan de él, directa o transitivamente, siempre que ya estén documentadas.
- No anticipes tareas para Features o Enablers aún no definidos documentalmente.

## Cobertura mínima

- Incluye tareas para las capas o áreas del sistema materialmente afectadas.
- Incluye tareas para contratos, persistencia, eventos, configuración, wiring, observabilidad, seguridad y pruebas cuando apliquen.
- Incluye tareas de integración entre componentes cuando el plan lo requiera.
- Incluye tareas documentales cuando la implementación afecte a cualquier fuente de verdad o documento operativo relevante.

## Disciplina de documentación

- La documentación debe quedar actualizada y consistente como parte de la ejecución de las tareas.
- Si la implementación derivada del plan cambia reglas globales, debe existir tarea para actualizar `docs/system/constitution.md`.
- Si cambia contexto operativo o restricciones del sistema, debe existir tarea para actualizar `docs/system/context.md`.
- Si introduce o aclara terminología compartida relevante, debe existir tarea para actualizar `docs/system/glossary.md`.
- Si cambia dependencias, baseline, propagación estructural o estado del roadmap, debe existir tarea para actualizar `docs/planning/dependency-graph.yaml` y `docs/planning/roadmap.md` cuando aplique.
- Si cambia el contexto mínimo, referencias normativas o slices documentales aplicables, debe existir tarea para actualizar `docs/planning/item-manifest.yaml`, `docs/planning/context-slices.yaml` y `docs/planning/adr-map.yaml` cuando aplique.
- Si la implementación evidencia una decisión técnica nueva o una modificación material de una existente, debe existir tarea para crear o actualizar el ADR correspondiente.
- Las tareas documentales deben limitarse a los artefactos materialmente afectados; no debe añadirse trabajo documental irrelevante.
- Si esta fase crea o actualiza artefactos documentales del item, debe incluir una tarea explícita para ejecutar `python tools/lint_sdd.py`.
- La fase no debe darse por cerrada mientras el conjunto documental afectado no pase el linter.

## Restricciones de contenido

- No incluyas código.
- No conviertas la lista en una reescritura de la especificación o del plan.
- No introduzcas decisiones arquitectónicas nuevas.
- No modifiques ADR existentes desde la propia lista de tareas.
- No introduzcas tecnologías no respaldadas por la documentación vigente.
- No generes tareas vagas, genéricas o difícilmente verificables.

## Manejo de bloqueos

- Si existen ambigüedades, contradicciones o dependencias no resueltas que impidan generar tareas fiables, márcalas explícitamente como pendientes de aclarar.
- No resuelvas bloqueos inventando comportamiento o decisiones técnicas no respaldadas.
- Los pendientes deben quedar formulados de manera concreta y accionable para que puedan resolverse antes de ejecutar la implementación.
