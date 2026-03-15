<!-- TEMPLATE: ADR -->

<!-- REQUIRED_FIELDS
ID
TITLE
STATUS
CONTEXT_DRIVER_1
DECISION_RULE_1
POSITIVE_CONSEQUENCE_1
VERIFICATION_1
PLAN_RULE_1
-->

# ADR-{{ID}}: {{TITLE}}

<<INSTRUCTION>>
Reemplazar {{ID}} y {{TITLE}}.

El título debe describir claramente la decisión técnica o arquitectónica adoptada.

Usar el mismo idioma que los ADR existentes del proyecto. En este repositorio, los ADR están redactados en inglés.

Eliminar todos los bloques <<INSTRUCTION>> en el documento final.
<<END_INSTRUCTION>>

## Status
{{STATUS}}

<<INSTRUCTION>>
Usar uno de los estados habituales del repositorio, por ejemplo:

- Proposed
- Accepted
- Superseded
- Deprecated

Si este ADR sustituye a otro, reflejarlo también en el contenido.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

## Context

{{CONTEXT_SUMMARY}}

<<INSTRUCTION>>
Describir el problema, restricciones, drivers y contexto que obligan a tomar esta decisión.

Puede incluir:

- restricciones operativas o de arquitectura
- referencias a constitution, context o ADR previos
- riesgos que se quieren evitar
- capacidades que deben preservarse

No convertir esta sección en la propia decisión.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

Key drivers:

- {{CONTEXT_DRIVER_1}}
- {{CONTEXT_DRIVER_2}}
- {{CONTEXT_DRIVER_3}}

## Decision

{{DECISION_SUMMARY}}

<<INSTRUCTION>>
Describir la decisión adoptada de forma normativa y vinculante.

Si aplica, usar lenguaje normativo como SHALL, MUST, MUST NOT, MAY o SHOULD para mantener consistencia con los ADR existentes.

Si la decisión tiene varias reglas internas, desglosarlas en subsecciones con títulos claros.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

- {{DECISION_RULE_1}}
- {{DECISION_RULE_2}}
- {{DECISION_RULE_3}}

This decision is normative and binding.

<<INSTRUCTION>>
Si el ADR necesita estructura adicional, añadir subsecciones dentro de Decision siguiendo el patrón de los ADR existentes, por ejemplo:

- Repository Structure
- Versioning Rules
- Persistence
- Delivery Semantics
- Error Mapping

Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

## Alternatives Considered

### 1. {{ALTERNATIVE_1}}

Rejected because:

- {{ALTERNATIVE_1_REASON_1}}
- {{ALTERNATIVE_1_REASON_2}}

### 2. {{ALTERNATIVE_2}}

Rejected because:

- {{ALTERNATIVE_2_REASON_1}}
- {{ALTERNATIVE_2_REASON_2}}

### 3. {{ALTERNATIVE_3}}

Rejected because:

- {{ALTERNATIVE_3_REASON_1}}
- {{ALTERNATIVE_3_REASON_2}}

<<INSTRUCTION>>
Mantener solo las alternativas que realmente se hayan considerado.
Si hay menos de tres, eliminar las secciones sobrantes.
Si una alternativa no fue rechazada sino pospuesta, indicarlo explícitamente.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

## Consequences

### Positive

- {{POSITIVE_CONSEQUENCE_1}}
- {{POSITIVE_CONSEQUENCE_2}}
- {{POSITIVE_CONSEQUENCE_3}}

### Negative / Trade-offs

- {{NEGATIVE_CONSEQUENCE_1}}
- {{NEGATIVE_CONSEQUENCE_2}}
- {{NEGATIVE_CONSEQUENCE_3}}

<<INSTRUCTION>>
Describir consecuencias reales de adoptar esta decisión.
No repetir el contexto ni la decisión; aquí deben quedar claros los efectos y trade-offs.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

### Operational Impact

- {{OPERATIONAL_IMPACT_1}}
- {{OPERATIONAL_IMPACT_2}}
- {{OPERATIONAL_IMPACT_3}}

<<INSTRUCTION>>
Incluir solo si la decisión tiene impacto operativo, de despliegue, observabilidad, CI, backup, mantenimiento o soporte.
Si no aplica, eliminar esta subsección.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

### Verification

Compliance is validated by:

- {{VERIFICATION_1}}
- {{VERIFICATION_2}}
- {{VERIFICATION_3}}

<<INSTRUCTION>>
Describir cómo se comprueba el cumplimiento de la decisión:

- CI
- contract tests
- code review
- linters
- migration checks
- runtime validation

Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

## Plan Enforcement

Any feature or enabler implementation plan affected by this ADR MUST:

- {{PLAN_RULE_1}}
- {{PLAN_RULE_2}}
- {{PLAN_RULE_3}}

If a plan violates these rules, it is invalid.

<<INSTRUCTION>>
Usar esta sección para traducir la decisión en disciplina práctica para planes e implementaciones futuras.
Si el ADR no requiere reglas explícitas de enforcement, puede mantenerse una versión mínima o eliminarse la sección.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>
