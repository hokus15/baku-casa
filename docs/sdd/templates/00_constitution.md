# Spec-Kit Prompt Template — `/speckit.constitution`

Genera la constitución del proyecto a partir de la definición contenida en:

`docs/system/constitution.md`

## Fuente autoritativa

- Usa exclusivamente `docs/system/constitution.md` como fuente de verdad.
- No cargues otros documentos de `docs/` salvo que el propio archivo referencie explícitamente otro artefacto imprescindible para resolver una referencia normativa.
- Si necesitas resolver una referencia explícita, carga solo el fragmento mínimo necesario.

## Reglas

- No inventes reglas nuevas.
- No elimines reglas existentes.
- No cambies el significado normativo de ninguna regla.
- Conserva la jerarquía normativa y la intención del documento original.
- Si mejoras redacción o estructura, hazlo solo para aumentar claridad sin alterar el contenido normativo.
- Mantén el lenguaje normativo del documento, incluyendo términos como `DEBE`, `NO DEBE`, `DEBERÍA` y `PUEDE` cuando existan.
- Mantén `docs/system/constitution.md` agnóstico al stack concreto.
- No introduzcas frameworks, librerías, herramientas o productos específicos en la constitución; si aparecen como decisión material, deben vivir en ADR.

## Disciplina de contexto

- Prioriza el uso mínimo de contexto.
- Trata `docs/system/constitution.md` como entrada suficiente por defecto.
- No añadas explicaciones, justificaciones ni contenido auxiliar que no provenga de la definición fuente.

## Validación documental

- Si esta fase modifica `docs/system/constitution.md`, debe ejecutarse `python tools/lint_sdd.py` antes de cerrarla.
- La fase no debe darse por completada si el linter documental falla.

