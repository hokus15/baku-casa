# EN-0301: Application Service Modularization

---

## Objetivo

Reorganizar los servicios de la capa Application en módulos coherentes por dominio o bounded context para mejorar la mantenibilidad, reforzar los límites arquitectónicos y evitar acoplamiento excesivo entre casos de uso.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- organización modular de la capa Application por dominios funcionales o bounded contexts
- reducción de dependencias cruzadas y mejora de cohesión entre casos de uso, puertos y DTOs de aplicación

El enabler afecta principalmente a:

- backend y estructura interna de la capa Application

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- cambios en reglas de negocio del Domain, contratos públicos de adaptadores o estrategias de persistencia
- introducción de nuevos bounded contexts o redefinición funcional del dominio más allá de la reorganización estructural

---

## Problema que resuelve

A medida que el sistema crece, la capa Application tiende a concentrar servicios y casos de uso en estructuras genéricas. Esto incrementa el riesgo de dependencias cruzadas no intencionales, crecimiento de módulos con responsabilidades dispares, duplicidad de conceptos y dificultad para localizar y evolucionar casos de uso. Sin una organización modular clara, la mantenibilidad y la claridad arquitectónica se degradan.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- la capa Application puede organizarse en módulos coherentes con fronteras explícitas y responsabilidades cohesionadas
- las dependencias entre módulos de Application quedan reducidas y se hacen explícitas
- el sistema puede evolucionar nuevos casos de uso preservando la arquitectura hexagonal y sin modificar el comportamiento funcional observable

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- cohesión y mantenibilidad de la capa Application del backend
- límites arquitectónicos entre módulos de aplicación, dominio y composition root

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler depende de:

- F-0009
- EN-0300

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

La lista anterior declara dependencias del item; este documento no sustituye la fuente estructural de dependencias.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0002 — Hexagonal Architecture
- ADR-0001 — Monorepo Multi-root

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- la capa Application está organizada en módulos coherentes por dominio o bounded context, con fronteras claras
- no existen módulos genéricos con responsabilidades dispares que concentren casos de uso sin cohesión
- las dependencias entre módulos de Application son mínimas y explícitas
- la reorganización no modifica el comportamiento funcional observable del sistema
- se mantienen las reglas de arquitectura hexagonal y la inversión de dependencias definida para el proyecto
