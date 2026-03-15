# Spec-Kit Prompt Template — `/speckit.clarify`

Aclara las zonas insuficientemente definidas de la especificación de un Roadmap Item antes de continuar con `speckit.plan`.

El item puede ser:

- una Feature
- un Enabler

El objetivo es dejar la especificación suficientemente clara, consistente y completa para permitir planificación e implementación sin ambigüedades evitables.

## Entrada principal

Usa como documento principal la especificación actual del item:

- `docs/specs/features/<feature-file>.md`, o
- `docs/specs/enablers/<enabler-file>.md`

## Contexto mínimo permitido

Resuelve primero el contexto mínimo del item con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase clarify --profile minimal`

La salida de esa utilidad es la entrada base obligatoria de esta fase.

Usa como contexto mínimo exactamente los artefactos devueltos por esa utilidad para el item y la fase actual.

Solo amplía el contexto si los artefactos resueltos no bastan para aclarar una ambigüedad real.

Debes asumir como baseline técnico aplicable el bloque `Core technical baseline` devuelto por la utilidad. Usa `Supporting technical baseline` y `Supporting ADRs` solo cuando una ambigüedad real requiera profundizar.

Prioriza primero `Direct dependencies` como baseline funcional inmediato del item. Usa `Transitive baseline dependencies` solo cuando una ambigüedad dependa de capacidades heredadas propagadas por el DAG.

Interpreta `Direct shared specs` como contratos compartidos explícitos del item. Consulta `Inherited shared specs` solo cuando una ambigüedad dependa de una semántica compartida heredada por dependencias.

Interpreta `Core constitution sections` y `Core context sections` como el contexto normativo y operativo explícitamente canónico del item. Usa `Supporting constitution sections` y `Supporting context sections` solo cuando los slices aporten baseline adicional necesario para resolver una ambigüedad real.

En esta fase, si necesitas profundizar manualmente, prioriza ADRs cuyo `reason` afecte a contrato, semántica de dominio o comportamiento observable; evita cargar ADRs de delivery u operación si no son necesarios.

No cargues por defecto el resto de `docs/`.

## Qué debes aclarar

- ambigüedades de comportamiento
- definiciones incompletas
- inconsistencias internas de la especificación
- contradicciones con fuentes autoritativas
- dependencias implícitas no declaradas
- huecos de terminología compartida
- supuestos que impedirían un `speckit.plan` fiable

## Reglas

- Basa la clarificación exclusivamente en la especificación del item y en las fuentes autoritativas mínimas necesarias para resolver ambigüedades.
- No inventes comportamiento que no esté definido, implícito de forma razonable o exigido por una regla global aplicable.
- No introduzcas dependencias no respaldadas por `docs/planning/dependency-graph.yaml`.
- No redefinas reglas globales ya definidas en `docs/system/constitution.md`; refiérelas o especialízalas solo si el item lo requiere.
- Reutiliza definiciones existentes de `docs/specs/shared/` cuando apliquen y no las dupliques.
- Mantén consistencia con la terminología de `docs/system/glossary.md` cuando aplique.
- Mantén consistencia con el contexto operativo definido en `docs/system/context.md`.
- Mantén consistencia con ADRs relevantes sin reescribir su contenido.

## Disciplina de documentación

- La documentación debe quedar actualizada y consistente tras el proceso de clarificación.
- Si la clarificación revela una regla global nueva o una modificación de una existente, debe actualizarse `docs/system/constitution.md`.
- Si la clarificación revela una restricción operativa, hecho del sistema o contexto global nuevo o modificado, debe actualizarse `docs/system/context.md`.
- Si la clarificación introduce o aclara terminología compartida relevante, debe actualizarse `docs/system/glossary.md`.
- Si la clarificación cambia dependencias, baseline o propagación estructural, debe actualizarse `docs/planning/dependency-graph.yaml`.
- Si la clarificación cambia el contexto mínimo, referencias normativas o slices documentales aplicables, deben actualizarse los artefactos de planificación correspondientes, incluyendo `docs/planning/item-manifest.yaml`, `docs/planning/context-slices.yaml` y `docs/planning/adr-map.yaml` cuando aplique.
- Si la especificación entra en conflicto con la documentación existente, no debe ignorarse el conflicto: la documentación afectada debe corregirse.
- No debe asumirse que la documentación actual es correcta si la clarificación demuestra que está desactualizada.
- Las actualizaciones documentales deben limitarse a los artefactos materialmente afectados; no debe reescribirse documentación no relacionada.
- Debe ejecutarse `python tools/lint_sdd.py` al final de la fase para validar que la documentación resultante sigue siendo consistente.
- La fase no debe cerrarse si el linter documental falla.

## Dependencias y baseline

- Analiza `docs/planning/dependency-graph.yaml` antes de clarificar el item.
- Si el item es una Feature, debe asumirse como baseline toda capacidad previa aplicable propagada por el grafo.
- La clarificación no debe ignorar Enablers ya aplicables ni duplicar capacidades ya introducidas.
- Si el item es un Enabler, debes tener en cuenta el impacto de la clarificación sobre Features existentes que dependan de él, directa o transitivamente, siempre que ya estén documentadas.
- No anticipes cambios en Features o Enablers aún no definidos documentalmente.

## Restricciones de contenido

- No propongas implementación técnica.
- No introduzcas decisiones de arquitectura nuevas salvo que la clarificación evidencie un hueco documental que requiera ADR.
- No modifiques ADR existentes desde la propia clarificación.
- No introduzcas tecnologías o frameworks.
- No rediseñes el item más allá de lo necesario para aclarar su comportamiento esperado.

## Manejo de ambigüedad residual

- Si después de aplicar las fuentes autoritativas mínimas siguen existiendo ambigüedades no resolubles, márcalas explícitamente como pendientes de aclarar.
- No resuelvas ambigüedades inventando comportamiento.
- Deja los pendientes formulados de manera concreta y accionable para que bloqueen explícitamente `speckit.plan` hasta su resolución.
