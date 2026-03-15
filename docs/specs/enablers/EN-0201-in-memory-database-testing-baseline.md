# EN-0201: In-Memory Database Testing Baseline

---

## Objetivo

Establecer un baseline de testing que permita ejecutar tests de integración con base de datos en memoria de forma rápida, reproducible y aislada, con configuración separada del runtime normal y sin dependencias externas.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- ejecución reproducible de tests de integración con persistencia real sobre una base de datos transitoria
- aislamiento determinista del estado de persistencia entre pruebas y compatibilidad con CI

El enabler afecta principalmente a:

- backend, testing de persistencia y validación de integración local y en CI

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- performance benchmarking, tests end-to-end dependientes de servicios externos o cambios en la lógica de negocio
- selección cerrada de framework de testing o definición de herramientas de migración más allá de exigir un esquema determinista para pruebas

---

## Problema que resuelve

El sistema requiere tests que verifiquen integración real con persistencia, como transacciones, repositorios y consultas, sin introducir dependencias externas ni complejidad operativa. Sin un baseline común para pruebas con base de datos en memoria, el feedback es más lento, el aislamiento entre tests puede degradarse y la reproducibilidad entre ejecución local y CI queda comprometida.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- los tests de integración pueden ejecutar escenarios reales de persistencia usando una base de datos en memoria y sin depender de servicios externos
- el esquema utilizado en testing se inicializa de forma determinista y consistente con el modelo persistente
- la suite de pruebas con base de datos puede ejecutarse con aislamiento entre tests y con resultados reproducibles en local y en CI

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- estrategia de testing de integración del backend
- configuración de testing y validación de persistencia en entornos locales y CI

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler puede depender de:

- EN-0202
- ninguna otra dependencia estructural definida para este enabler

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0003 — Persistence SQLite SQLAlchemy
- ADR-0013 — Configuration System

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- los tests de integración pueden ejecutarse utilizando una base de datos en memoria sin dependencias externas adicionales
- el esquema de base de datos para testing se inicializa de forma determinista y consistente
- los tests con persistencia quedan aislados entre sí y no dependen del estado generado por otras pruebas
- existe una configuración de testing explícita y separada para habilitar la base de datos en memoria sin ambigüedad con el runtime normal
- la ejecución local y la ejecución en CI producen resultados consistentes
