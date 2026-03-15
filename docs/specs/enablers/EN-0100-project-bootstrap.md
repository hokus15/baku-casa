# EN-0100: Project Bootstrap

---

## Objetivo

Establecer la base mínima del repositorio para habilitar el desarrollo reproducible mediante Specification Driven Development (SDD) antes de implementar cualquier funcionalidad de dominio.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- inicialización estructural del monorepo multi-root
- validación técnica mínima por root y baseline documental del proyecto

El enabler afecta principalmente a:

- backend, bot y baseline de project bootstrap del repositorio

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- cualquier caso de uso, lógica de negocio o funcionalidad de dominio
- persistencia funcional, endpoints reales o automatizaciones avanzadas de CI más allá del baseline mínimo

---

## Problema que resuelve

Antes de este enabler, el sistema no dispone de una base técnica mínima y consistente para empezar a evolucionar mediante SDD. Sin una estructura inicial de proyecto, una organización documental básica y una validación mínima automatizada, el desarrollo de futuras features carece de un punto de partida reproducible, verificable y alineado con la gobernanza del sistema.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- el repositorio dispone de una estructura inicial multi-root estable sobre la que pueden incorporarse nuevas capacidades sin mezclar todavía lógica de dominio
- cada root del proyecto puede validarse de forma independiente mediante una verificación mínima reproducible
- el sistema cuenta con una base documental y operativa suficiente para sostener la evolución posterior de features y enablers

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- estructura del repositorio y organización inicial del monorepo
- gobernanza técnica, validación continua y documentación base del sistema

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler puede depender de:

- ninguna
- ninguna dependencia previa definida en el sistema

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0001 — Monorepo Multi-root
- ADR-0008 — CI and Governance Model

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- existe una estructura multi-root con `backend/` y `bot/`, y cada root dispone de una base mínima para código y pruebas
- existen un `README.md` en la raíz y los directorios documentales base necesarios para iniciar el trabajo guiado por especificaciones
- existe una validación continua mínima que ejecuta comprobaciones por root en cada pull request
- existen pruebas mínimas por root que validan que el runner de tests funciona correctamente
- el resultado del enabler no introduce funcionalidades de dominio ni endpoints reales
