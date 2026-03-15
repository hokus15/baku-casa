# Spec-Kit Prompt Template — `/speckit.specify`

Genera la especificación de un Roadmap Item a partir de su definición fuente.

El item puede ser:

- una Feature
- un Enabler

## Entrada principal

Usa como documento principal la definición fuente del item:

- `docs/specs/features/<feature-file>.md`, o
- `docs/specs/enablers/<enabler-file>.md`

## Contexto mínimo permitido

Resuelve primero el contexto mínimo del item con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase specify --profile minimal`

La salida de esa utilidad es la entrada base obligatoria de esta fase.

Usa como contexto mínimo exactamente los artefactos devueltos por esa utilidad para el item y la fase actual.

Solo amplía el contexto si los artefactos resueltos no bastan para completar la fase con seguridad.

Debes asumir como baseline técnico aplicable el bloque `Core technical baseline` devuelto por la utilidad. Usa `Supporting technical baseline` y `Supporting ADRs` solo cuando necesites profundizar para especificar sin ambigüedad.

Prioriza primero `Direct dependencies` como baseline funcional inmediato del item. Usa `Transitive baseline dependencies` solo cuando necesites confirmar capacidades heredadas propagadas por el DAG.

Interpreta `Direct shared specs` como contratos compartidos explícitos del item. Consulta `Inherited shared specs` solo cuando una dependencia directa o transitiva haga necesario reutilizar una semántica compartida ya establecida.

Interpreta `Core constitution sections` y `Core context sections` como el contexto normativo y operativo explícitamente canónico del item. Usa `Supporting constitution sections` y `Supporting context sections` solo cuando los slices aporten baseline adicional realmente necesario.

En esta fase, si necesitas profundizar manualmente, prioriza ADRs cuyo `reason` afecte al contrato o semántica del item.

No cargues por defecto el resto de `docs/`.

## Reglas

- Basa la especificación exclusivamente en la definición fuente del item y en las fuentes autoritativas mínimas necesarias para mantener consistencia.
- No inventes comportamiento que no esté definido, implícito de forma razonable o exigido por una regla global aplicable.
- No inventes dependencias; usa únicamente `docs/planning/dependency-graph.yaml` cuando sea necesario resolverlas.
- No redefinas reglas globales ya definidas en `docs/system/constitution.md`; refiérelas o especialízalas solo si el item lo requiere.
- Reutiliza definiciones existentes de `docs/specs/shared/` cuando apliquen y no las dupliques.
- Mantén consistencia con la terminología de `docs/system/glossary.md` cuando aplique.
- Mantén consistencia con el contexto operativo definido en `docs/system/context.md`.
- Mantén consistencia con ADRs relevantes sin reescribir su contenido.

## Disciplina de documentación

- La documentación debe quedar actualizada y consistente tras generar o revisar la especificación.
- Si la definición del item revela una regla global nueva o una modificación de una existente, debe actualizarse `docs/system/constitution.md`.
- Si la definición del item revela una restricción operativa, hecho del sistema o contexto global nuevo o modificado, debe actualizarse `docs/system/context.md`.
- Si la definición del item introduce o aclara terminología compartida relevante, debe actualizarse `docs/system/glossary.md`.
- Si la definición del item cambia dependencias, baseline o propagación estructural, debe actualizarse `docs/planning/dependency-graph.yaml`.
- Si la definición del item cambia el contexto mínimo, referencias normativas o slices documentales aplicables, deben actualizarse los artefactos de planificación correspondientes, incluyendo `docs/planning/item-manifest.yaml`.
- Si la definición del item entra en conflicto con la documentación existente, no debe ignorarse el conflicto: la documentación afectada debe corregirse.
- No debe asumirse que la documentación actual es correcta si la definición fuente del item demuestra que está desactualizada.
- Las actualizaciones documentales deben limitarse a los artefactos materialmente afectados; no debe reescribirse documentación no relacionada.
- Debe ejecutarse `python tools/lint_sdd.py` al final de la fase para validar que la documentación resultante sigue siendo consistente.
- La fase no debe cerrarse si el linter documental falla.

## Restricciones de contenido

- No introduzcas decisiones técnicas ni detalles de implementación.
- Describe comportamiento esperado del sistema, alcance, reglas e invariantes del item.
- Si el item es una Feature, describe comportamiento funcional de dominio.
- Si el item es un Enabler, describe capacidad técnica del sistema sin introducir funcionalidad de dominio.

## Manejo de ambigüedad

- Si la definición fuente es ambigua, incompleta o contradice una fuente autoritativa relevante, marca explícitamente los puntos afectados como pendientes de aclarar.
- No resuelvas ambigüedades inventando comportamiento.
- Deja los pendientes formulados de manera que puedan ser tratados posteriormente por `speckit.clarify`.
