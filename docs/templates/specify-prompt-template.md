Genera la especificación para la Feature <N>: "<Título>".

## Fuentes Autoritativas

La definición funcional debe obtenerse exclusivamente del documento:
- docs/spec/features/<nombre-fichero-feature>.md

Debe considerarse además:
- docs/spec/context.md
- docs/spec/roadmap.md
- docs/adr/ADR-0001..ADR-0012

La especificación NO puede contradecir ningún ADR ni la Constitución.

Si la Feature requiere modificar o crear un ADR, debe indicarse explícitamente en una sección "ADR Gap".

---

## Disciplina de ADR

Todas las Features deben cumplir TODOS los ADR vigentes.

Sin embargo:

- Solo deben mencionarse explícitamente en el documento aquellos ADR que se vean materialmente impactados por esta Feature.
- Si un ADR no es relevante para esta Feature, no debe forzarse su referencia.
- Si la Feature afecta contratos (API o eventos), debe indicarse claramente el impacto en versionado.
- Si la Feature introduce eventos, debe referenciar ADR-0010 obligatoriamente.
- Si la Feature introduce cambios persistentes, debe referenciar ADR-0003.

---

## Restricciones Importantes

1. No contradigas ningún ADR.
2. No incluyas decisiones técnicas ya cubiertas por ADR.
3. Define únicamente el QUÉ, no el CÓMO.
4. No menciones frameworks, estructura de código, ORM, Docker ni CI.
5. Si la Feature impacta contratos (API o eventos), debe quedar claro el impacto en versionado.
6. Si introduce eventos, debe respetar CloudEvents y versionado.
7. Si introduce persistencia nueva, debe respetar disciplina transaccional.
8. Dinero y porcentajes deben respetar representación Decimal y rango 0–100.
9. Todos los tiempos deben asumirse UTC.
10. Los errores deben ser tipificados.

Disciplina ADR:

- Todas las Features deben cumplir todos los ADR.
- Solo deben mencionarse explícitamente los ADR materialmente impactados.
- Si la Feature requiere un nuevo ADR o modificación de uno existente, debe indicarse claramente como "ADR Gap".
