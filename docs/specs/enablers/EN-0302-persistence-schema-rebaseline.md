# EN-0302: Persistence Schema Rebaseline

---

## Objetivo

Consolidar el esquema de persistencia al finalizar MVP1, reemplazando el historial inicial de migraciones por un baseline limpio del esquema de base de datos para simplificar la evolución futura del sistema antes de introducir el núcleo financiero.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- consolidación del esquema de persistencia tras estabilizar el modelo de MVP1
- establecimiento de un nuevo baseline de migraciones coherente y recreable desde cero

El enabler afecta principalmente a:

- backend, persistencia y baseline de migraciones previo al inicio de MVP2

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- cambios en el modelo de dominio, en la lógica de negocio o introducción de nuevas entidades funcionales
- preservación o migración de datos existentes fuera del objetivo de consolidar el esquema y su historial de migraciones

---

## Problema que resuelve

Durante MVP1 el modelo de persistencia evoluciona de forma iterativa mientras se explora y estabiliza el dominio. Como resultado, el historial de migraciones puede acumular cambios intermedios, estructuras temporales, inconsistencias de naming o constraints y migraciones exploratorias ya obsoletas. Sin una consolidación explícita antes de iniciar MVP2, la base de persistencia para el núcleo financiero queda innecesariamente compleja y frágil.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- el sistema dispone de un baseline limpio del esquema de persistencia alineado con el estado final de MVP1
- el esquema completo de la base de datos puede recrearse desde cero a partir de un nuevo punto de partida coherente
- las migraciones posteriores pueden evolucionar desde una base estabilizada y preparada para soportar el núcleo financiero

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- historial de migraciones y baseline del esquema de persistencia
- preparación técnica del backend para iniciar MVP2 sobre una base de datos estabilizada

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler depende de:

- F-0009
- ninguna otra dependencia estructural definida para este enabler

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

La lista anterior declara dependencias del item; este documento no sustituye la fuente estructural de dependencias.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0003 — Persistence SQLite SQLAlchemy
- ADR-0002 — Hexagonal Architecture

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- existe un nuevo baseline inicial que representa el estado consolidado del esquema tras MVP1
- el esquema completo de la base de datos puede recrearse desde cero utilizando únicamente ese nuevo baseline
- el historial previo de migraciones exploratorias ha sido eliminado o archivado
- el resultado no introduce cambios funcionales en el comportamiento del sistema
- el nuevo baseline de persistencia puede utilizarse como punto de partida para las migraciones de MVP2
