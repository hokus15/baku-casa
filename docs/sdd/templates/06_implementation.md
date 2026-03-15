# Spec-Kit Prompt Template — `/speckit.implement`

Ejecuta todas las tareas necesarias para construir el item según la especificación, la clarificación vigente, el plan técnico y la lista de tareas aprobada.

El item puede ser:

- una Feature
- un Enabler

El objetivo es materializar el item en el sistema real respetando el baseline existente, las decisiones arquitectónicas vigentes y las reglas documentales del proyecto.

## Entradas principales

Usa como entradas principales todos los artefactos vigentes del item que deben existir en este punto del flujo:

- la especificación vigente del item
- los resultados de clarificación del item, si existen
- el plan técnico vigente del item
- la lista de tareas vigente del item
- los hallazgos de `speckit.analyze`, si existen

## Contexto mínimo permitido

Resuelve primero el contexto mínimo del item con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase implement --profile deep`

La salida de esa utilidad es la entrada base obligatoria de esta fase.

Usa como contexto mínimo exactamente los artefactos devueltos por esa utilidad para el item y la fase actual, junto con los artefactos vigentes del item.

Solo amplía el contexto si los artefactos resueltos no bastan para implementar con seguridad.

Debes tratar el bloque `Core technical baseline` devuelto por la utilidad como el stack efectivo autorizado para el item en esta fase. Usa `Supporting technical baseline` y `Supporting ADRs` solo cuando la implementación necesite concretar una restricción o integración adicional.

Prioriza primero `Direct dependencies` al materializar integraciones y reusar capacidades existentes. Usa `Transitive baseline dependencies` solo cuando la implementación necesite confirmar una capacidad heredada más lejana del DAG.

Interpreta `Direct shared specs` como contratos compartidos de aplicación directa durante la implementación. Usa `Inherited shared specs` solo cuando sea necesario respetar una semántica compartida heredada por baseline.

Interpreta `Core constitution sections` y `Core context sections` como el baseline normativo y operativo directo del item. Usa `Supporting constitution sections` y `Supporting context sections` solo cuando la implementación necesite baseline adicional aportado por los slices.

En esta fase, si necesitas profundizar manualmente, usa `reason` para cargar en detalle solo los ADRs con impacto directo en la implementación material.

No cargues por defecto el resto de `docs/`.

## Qué debe hacerse

- ejecutar las tareas aprobadas del item
- implementar el comportamiento o capacidad definida por la especificación
- respetar las aclaraciones y restricciones ya resueltas en `clarify`
- seguir el plan técnico vigente
- resolver los hallazgos de `analyze` antes o durante la implementación cuando sean bloqueantes
- dejar el código, las pruebas y la documentación en un estado consistente con el sistema real

## Reglas

- Basa la implementación exclusivamente en la especificación, clarificación, plan, tareas y fuentes autoritativas mínimas necesarias para ejecutar el trabajo correctamente.
- Implementa usando el stack tecnológico ya adoptado por el proyecto; no introduzcas tecnologías nuevas salvo que una fuente autoritativa vigente las respalde o se haya aprobado el ADR correspondiente.
- No inventes comportamiento funcional que no esté definido, implícito de forma razonable o exigido por una regla global aplicable.
- No introduzcas dependencias no respaldadas por `docs/planning/dependency-graph.yaml`.
- No redefinas reglas globales ya definidas en `docs/system/constitution.md`; la implementación debe respetarlas.
- Mantén consistencia con la terminología de `docs/system/glossary.md` cuando aplique.
- Mantén consistencia con ADRs relevantes y con las convenciones vigentes del proyecto.

## Dependencias y baseline

- Verifica `docs/planning/dependency-graph.yaml` antes de implementar.
- No implementes el item ignorando dependencias previas no satisfechas.
- Si el item es una Feature, asume como baseline las capacidades previas aplicables propagadas por el grafo.
- No dupliques capacidades técnicas ya introducidas por Enablers existentes.
- Si el item es un Enabler, implementa teniendo en cuenta su impacto sobre Features existentes documentadas cuando ese impacto ya esté reflejado en los artefactos vigentes.
- No anticipes implementación de Features o Enablers aún no definidos documentalmente.

## Cobertura mínima de implementación

- Implementa todas las tareas aprobadas materialmente necesarias para completar el item.
- Incluye cambios en dominio, aplicación, interfaces, persistencia, configuración, wiring, observabilidad, seguridad y pruebas cuando el plan o las tareas lo requieran.
- Asegura que la implementación preserve contratos, invariantes y compatibilidad según la documentación vigente.
- Si `speckit.analyze` detectó huecos o contradicciones bloqueantes, no los ignores durante la implementación.

## Disciplina de documentación

- La documentación debe quedar actualizada y consistente con el sistema implementado.
- Si la implementación cambia reglas globales, debe actualizarse `docs/system/constitution.md`.
- Si cambia contexto operativo o restricciones del sistema, debe actualizarse `docs/system/context.md`.
- Si introduce o aclara terminología compartida relevante, debe actualizarse `docs/system/glossary.md`.
- Si cambia dependencias, baseline, propagación estructural o estado del roadmap, deben actualizarse `docs/planning/dependency-graph.yaml` y `docs/planning/roadmap.md` cuando aplique.
- Si cambia el contexto mínimo, referencias normativas o slices documentales aplicables, deben actualizarse `docs/planning/item-manifest.yaml`, `docs/planning/context-slices.yaml` y `docs/planning/adr-map.yaml` cuando aplique.
- Si la implementación evidencia una decisión técnica nueva o una modificación material de una existente, debe crearse o actualizarse el ADR correspondiente.
- Si la implementación obliga a ajustar la especificación del item, ese cambio no debe introducirse de forma implícita: debe quedar reflejado en el artefacto documental correspondiente.
- Las actualizaciones documentales deben limitarse a los artefactos materialmente afectados; no debe reescribirse documentación no relacionada.
- Si la implementación crea o modifica cualquier archivo dentro de `docs/`, debe ejecutarse `python tools/lint_sdd.py` antes de cerrar la fase.
- La implementación no debe darse por completada mientras el linter documental falle.

## Restricciones de contenido y ejecución

- No contradigas la especificación funcional vigente.
- No ignores pendientes de aclarar o hallazgos bloqueantes como si estuvieran resueltos.
- No introduzcas decisiones arquitectónicas nuevas sin el soporte documental correspondiente.
- No modifiques ADR existentes desde la propia implementación sin pasar por el proceso documental adecuado.
- No introduzcas tecnologías no respaldadas por la documentación vigente.

## Manejo de bloqueos

- Si durante la implementación aparece una contradicción entre especificación, clarificación, plan, tareas o fuentes autoritativas, detén la suposición implícita y marca el bloqueo explícitamente.
- Si un bloqueo requiere nueva aclaración, debe marcarse como pendiente de aclarar.
- Si un bloqueo requiere decisión arquitectónica, debe marcarse como hueco de ADR.
- No resuelvas bloqueos inventando comportamiento o decisiones técnicas no respaldadas.
