# EN-{{ID}}: {{TITLE}}

<<INSTRUCTION>>
Reemplazar {{ID}} y {{TITLE}}.
El título debe describir la capacidad técnica introducida.
Eliminar este bloque de instrucciones en el documento final.
<<END_INSTRUCTION>>

---

## Objetivo

{{OBJECTIVE}}

<<INSTRUCTION>>
Describir brevemente qué capacidad técnica introduce el enabler y por qué es necesario.
No describir implementación.
Eliminar este bloque en el resultado final.
<<END_INSTRUCTION>>

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- {{SCOPE_CAPABILITY_1}}
- {{SCOPE_CAPABILITY_2}}

El enabler afecta principalmente a:

- {{AFFECTED_AREA}}

Este enabler **NO introduce cambios funcionales en el dominio**.

<<INSTRUCTION>>
Indicar las áreas del sistema afectadas (ej: backend, arquitectura, observabilidad).
Eliminar este bloque en el resultado final.
<<END_INSTRUCTION>>

---

## Problema que resuelve

{{PROBLEM_DESCRIPTION}}

<<INSTRUCTION>>
Explicar la limitación o problema técnico que motiva el enabler.
Eliminar este bloque en el resultado final.
<<END_INSTRUCTION>>

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- {{CAPABILITY_1}}
- {{CAPABILITY_2}}
- {{CAPABILITY_3}}

La capacidad debe describirse **en términos de resultado**, no de implementación.

<<INSTRUCTION>>
Describir la capacidad que estará disponible una vez implementado el enabler.
Eliminar este bloque en el resultado final.
<<END_INSTRUCTION>>

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- {{IMPACT_AREA_1}}
- {{IMPACT_AREA_2}}

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler puede depender de:

- {{DEPENDENCY_1}}
- {{DEPENDENCY_2}}

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- {{ADR_REFERENCE_1}}
- {{ADR_REFERENCE_2}}

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- {{ACCEPTANCE_CRITERION_1}}
- {{ACCEPTANCE_CRITERION_2}}
- {{ACCEPTANCE_CRITERION_3}}

<<INSTRUCTION>>
Los criterios deben describir condiciones observables que indiquen que el enabler está completado.
Eliminar este bloque en el resultado final.
<<END_INSTRUCTION>>

---

## Notas de implementación (opcional)

{{IMPLEMENTATION_NOTES}}

<<INSTRUCTION>>
Sección opcional. Puede omitirse si no es necesaria.
Eliminar este bloque en el resultado final.
<<END_INSTRUCTION>>