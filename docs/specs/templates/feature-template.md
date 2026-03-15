<!-- TEMPLATE: FEATURE_SPEC -->

<!-- REQUIRED_FIELDS
ID
TITLE
OBJECTIVE
PRIMARY_ENTITY
CAPABILITY_1
ACCEPTANCE_CRITERION_1
-->

# F-{{ID}}: {{TITLE}}

<<INSTRUCTION>>
Reemplazar {{ID}} y {{TITLE}}.

El título debe describir claramente la capacidad funcional introducida.

Eliminar todos los bloques <<INSTRUCTION>> en el documento final.
<<END_INSTRUCTION>>

---

## Objetivo

{{OBJECTIVE}}

<<INSTRUCTION>>
Describir qué capacidad funcional introduce esta feature y qué problema del dominio resuelve.

No describir implementación técnica.
No fijar decisiones tecnológicas concretas; si una decisión técnica condiciona la feature, debe referenciarse mediante ADR o shared spec aplicable.
<<END_INSTRUCTION>>

---

## Alcance

Esta feature cubre:

- {{IN_SCOPE_1}}
- {{IN_SCOPE_2}}
- {{IN_SCOPE_3}}

<<INSTRUCTION>>
Describir qué comportamiento funcional sí forma parte de la feature.
El alcance debe expresarse en términos de capacidad de dominio observable.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Fuera de alcance

- {{OUT_OF_SCOPE_1}}
- {{OUT_OF_SCOPE_2}}
- {{OUT_OF_SCOPE_3}}

<<INSTRUCTION>>
Indicar explícitamente qué NO cubre esta feature.
Puede incluir automatizaciones futuras, variantes no soportadas o capacidades reservadas para otras features o enablers.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Definiciones

<<INSTRUCTION>>
Definir los conceptos de dominio que introduce la feature.
Referenciar docs/specs/shared cuando corresponda.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

- {{DOMAIN_TERM_1}}
- {{DOMAIN_TERM_2}}
- {{DOMAIN_TERM_3}}

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- {{PRIMARY_ENTITY}}
- {{SECONDARY_ENTITY}}

<<INSTRUCTION>>
Las entidades deben ser conceptos del dominio, no modelos técnicos.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Datos principales

La feature gestiona la siguiente información:

- {{DATA_FIELD_1}}
- {{DATA_FIELD_2}}
- {{DATA_FIELD_3}}

<<INSTRUCTION>>
Describir los campos conceptuales relevantes.
No describir estructuras de base de datos.
No introducir restricciones de persistencia, concurrencia, índices o framework salvo que formen parte del comportamiento observable o se referencien desde una fuente autoritativa.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Capacidades

La feature debe permitir:

- {{CAPABILITY_1}}
- {{CAPABILITY_2}}
- {{CAPABILITY_3}}

<<INSTRUCTION>>
Las capacidades deben describir comportamiento observable del sistema.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Reglas del dominio

La feature debe respetar las siguientes reglas:

- {{DOMAIN_RULE_1}}
- {{DOMAIN_RULE_2}}
- {{DOMAIN_RULE_3}}

<<INSTRUCTION>>
Estas reglas deben describir invariantes o comportamiento del dominio.
No incluir reglas técnicas de implementación.
Si una regla global ya existe en `docs/system/constitution.md`, debe referenciarse o especializarse sin reescribirla.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- {{EDGE_CASE_1}}
- {{EDGE_CASE_2}}
- {{EDGE_CASE_3}}

<<INSTRUCTION>>
Describir situaciones límite que puedan afectar al comportamiento del sistema.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Dependencias

Esta feature puede depender de:

- {{DEPENDENCY_1}}
- {{DEPENDENCY_2}}

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/{{SHARED_SPEC_1}}
- docs/specs/shared/{{SHARED_SPEC_2}}

<<INSTRUCTION>>
Referenciar shared specs realmente aplicables a esta feature.
Si no aplica ninguno, sustituir la frase anterior y la lista por:

Esta feature no requiere shared specs adicionales en su definición actual.

Evitar formulaciones opcionales como "puede reutilizar".
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Relación con fuentes autoritativas

Esta feature puede requerir interpretación conjunta con:

- `docs/system/constitution.md`
- `docs/system/context.md`
- `docs/decisions/adr/{{ADR_REFERENCE_1}}`
- `docs/decisions/adr/{{ADR_REFERENCE_2}}`

<<INSTRUCTION>>
Incluir solo las referencias materialmente necesarias para interpretar la feature.
No duplicar el contenido de constitution, context o ADR; referenciarlos.
Si no hay ADR materialmente relevante, eliminar las líneas de ADR y dejar solo las fuentes realmente aplicables.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>

---

## Criterios de aceptación

La feature se considera completada cuando:

- {{ACCEPTANCE_CRITERION_1}}
- {{ACCEPTANCE_CRITERION_2}}
- {{ACCEPTANCE_CRITERION_3}}

<<INSTRUCTION>>
Los criterios deben describir condiciones observables que indiquen que la feature funciona correctamente.
Eliminar este bloque en el documento final.
<<END_INSTRUCTION>>
