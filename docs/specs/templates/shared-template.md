<!-- TEMPLATE: SHARED_SPEC -->

<!-- REQUIRED_FIELDS
ID
TITLE
OBJECTIVE
SHARED_RULE_1
CONSUMER_SPEC_1
-->

# SHARED-{{ID}}: {{TITLE}}

<<INSTRUCTION>>
Reemplazar {{ID}} y {{TITLE}}.

El título debe describir claramente el concepto, contrato o catálogo compartido.

Eliminar todos los bloques <<INSTRUCTION>> en el documento final.
<<END_INSTRUCTION>>

---

## Objetivo

{{OBJECTIVE}}

<<INSTRUCTION>>
Describir qué definición compartida introduce este documento y por qué conviene centralizarla.

Debe quedar claro que este documento existe para evitar duplicación entre múltiples specs.
No describir implementación técnica.
<<END_INSTRUCTION>>

---

## Ámbito de uso

Este shared spec aplica cuando múltiples features o enablers necesitan reutilizar exactamente la misma definición, contrato o catálogo.

Se utiliza como referencia común para evitar divergencias entre especificaciones.

<<INSTRUCTION>>
Indicar de forma explícita en qué casos debe usarse este shared spec y en cuáles no.
Si aplica solo a un subconjunto del dominio, dejarlo claro.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Definiciones

- {{TERM_1}}
- {{TERM_2}}
- {{TERM_3}}

<<INSTRUCTION>>
Definir aquí los conceptos compartidos mínimos necesarios para interpretar el documento.
Si el shared spec es un catálogo puro, esta sección puede describir la semántica de cada tipo o valor.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Contenido compartido

Este documento centraliza los siguientes elementos reutilizables:

- {{SHARED_ELEMENT_1}}
- {{SHARED_ELEMENT_2}}
- {{SHARED_ELEMENT_3}}

<<INSTRUCTION>>
Describir qué se está centralizando: vocabulario, contrato observable, lista cerrada, semántica común, etc.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Reglas compartidas

Este shared spec define las siguientes reglas reutilizables:

- {{SHARED_RULE_1}}
- {{SHARED_RULE_2}}
- {{SHARED_RULE_3}}

<<INSTRUCTION>>
Estas reglas deben ser reutilizables por varias specs.
No incluir detalles de implementación ni reglas globales que pertenezcan a constitution.md.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Contrato observable

Cuando este shared spec aplique, las especificaciones consumidoras deben respetar:

- {{OBSERVABLE_CONTRACT_1}}
- {{OBSERVABLE_CONTRACT_2}}
- {{OBSERVABLE_CONTRACT_3}}

<<INSTRUCTION>>
Describir qué comportamiento o contrato externo debe verse reflejado en las specs consumidoras.
Puede incluir nombres, formatos, semántica de campos, listas cerradas o condiciones observables.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Referencias normativas

Este shared spec puede apoyarse en:

- `docs/system/constitution.md` — {{CONSTITUTION_REFERENCE}}
- {{ADR_REFERENCE_1}}
- {{ADR_REFERENCE_2}}

<<INSTRUCTION>>
Referenciar solo fuentes autoritativas realmente necesarias.
No duplicar aquí el contenido de constitution o ADR; este documento debe especializar o reutilizar, no reescribir.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Specs consumidoras

Este shared spec puede ser referenciado por:

- docs/specs/features/{{CONSUMER_SPEC_1}}
- docs/specs/features/{{CONSUMER_SPEC_2}}
- docs/specs/enablers/{{CONSUMER_SPEC_3}}

<<INSTRUCTION>>
Listar las specs que deberían reutilizar este documento.
Si alguna todavía no existe, puede omitirse.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Criterios de adopción

Este shared spec se considera correctamente introducido cuando:

- {{ADOPTION_CRITERION_1}}
- {{ADOPTION_CRITERION_2}}
- {{ADOPTION_CRITERION_3}}

<<INSTRUCTION>>
Describir condiciones observables que indiquen que el documento ya puede actuar como fuente reutilizable.
Por ejemplo: existencia de catálogo estable, referencias desde specs consumidoras, ausencia de duplicación divergente.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Notas de mantenimiento (opcional)

{{MAINTENANCE_NOTES}}

<<INSTRUCTION>>
Sección opcional.
Puede incluir criterios para decidir cuándo ampliar este documento o cuándo una definición debe seguir viviendo en una spec individual.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>
