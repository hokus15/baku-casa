# EN-0300: HTTP Application Bootstrap Modularization

---

## Objetivo

Reducir el acoplamiento en el punto de entrada de la aplicación HTTP del backend separando las responsabilidades de inicialización y garantizando que el composition root siga siendo el único lugar donde se conectan interfaces de Application con implementaciones de Infrastructure.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- modularización estructural del bootstrap HTTP
- separación verificable de responsabilidades de arranque sin alterar la superficie funcional de la aplicación

El enabler afecta principalmente a:

- backend, bootstrap HTTP y composition root de la aplicación

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- cambios en la lógica de negocio, en los contratos de la API HTTP o en el comportamiento funcional observable del sistema
- introducción de nuevos middleware, routers o redefinición del modelo de dominio y de los servicios de aplicación

---

## Problema que resuelve

Actualmente el punto de entrada HTTP del backend concentra múltiples responsabilidades relacionadas con la inicialización de la aplicación, incluyendo creación de la aplicación, registro de dependencias, middleware, routers y manejadores de errores. Esta acumulación incrementa la complejidad del entrypoint, dificulta la mantenibilidad del composition root y vuelve menos trazable la evolución del bootstrap.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- el proceso de bootstrap de la aplicación HTTP queda separado en componentes con responsabilidades claras y trazables
- el point of entry HTTP puede limitarse a iniciar la aplicación y delegar el resto del bootstrap a componentes especializados
- el composition root conserva un único punto central para registrar dependencias entre capas y mantiene el comportamiento fail-fast ante errores críticos de arranque

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- estructura del bootstrap y mantenibilidad del adapter HTTP
- verificación arquitectónica de límites entre interfaces, application e infrastructure

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler depende de:

- EN-0202
- ninguna otra dependencia estructural definida para este enabler

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

La lista anterior declara dependencias del item; este documento no sustituye la fuente estructural de dependencias.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0002 — Hexagonal Architecture
- ADR-0013 — Configuration System

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- el punto de entrada HTTP deja de concentrar múltiples responsabilidades de inicialización
- el proceso de bootstrap de la aplicación queda separado en componentes con responsabilidades identificables y trazables
- el registro de dependencias entre capas sigue realizándose exclusivamente en el composition root
- los errores críticos durante el bootstrap provocan fallo inmediato del arranque, sin degradación silenciosa
- la reorganización no modifica la superficie funcional observable de la aplicación ni rompe los quality gates relevantes del backend
