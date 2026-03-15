# EN-0209: Idempotency and Duplicate Operation Protection

---

## Objetivo

Introducir una capacidad transversal de protección frente a ejecuciones duplicadas en operaciones con efecto económico para permitir reintentos seguros sin crear eventos, pagos u otros efectos persistentes duplicados.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- detección y bloqueo de ejecuciones repetidas de una misma operación lógica con efecto económico
- soporte operativo para reintentos seguros en APIs, automatizaciones o procesos internos que puedan repetir solicitudes

El enabler afecta principalmente a:

- backend y operaciones económicas críticas del ledger, incluyendo flujos de creación de devengos, pagos u otros efectos persistentes

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- resolución funcional de conflictos de negocio no relacionados con reintentos o duplicados técnicos
- sustitución de validaciones del dominio, del control transaccional o del baseline contable ya definido por las features económicas

---

## Problema que resuelve

Las operaciones económicas del sistema generan efectos persistentes que no pueden duplicarse sin comprometer la integridad del ledger y el cálculo de saldos. En presencia de reintentos de cliente, fallos de red, errores operativos o automatizaciones reejecutadas, el sistema necesita una capacidad común para reconocer la misma operación lógica y evitar que se materialice más de una vez.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- las operaciones críticas con efecto económico pueden ejecutarse de forma segura ante reintentos sin producir duplicados persistentes
- el sistema puede identificar solicitudes repetidas y decidir de forma determinista si deben reutilizar un resultado previo o bloquear la duplicidad
- las features que creen eventos económicos pueden apoyarse en una disciplina común de idempotencia sin implementar mecanismos ad hoc incompatibles entre sí

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- servicios de aplicación, persistencia y contratos de entrada de operaciones económicas críticas
- features financieras que generen hechos persistentes, incluyendo como mínimo F-0010 y F-0011

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler puede depender de:

- F-0010
- ninguna otra dependencia estructural definida para este enabler

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0014 — Idempotent Operations and Duplicate Protection
- ADR-0009 — Error Model and Observability

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- las operaciones económicas críticas pueden recibir reintentos de la misma operación lógica sin crear efectos económicos duplicados
- el sistema dispone de una forma consistente de identificar duplicados en los flujos protegidos y de aplicar una respuesta determinista ante repeticiones
- los intentos duplicados, rechazos o reutilizaciones relevantes quedan trazados operativamente de forma suficiente para diagnóstico y soporte
- las features que dependan de este enabler pueden apoyarse en una base común de protección contra duplicados sin introducir mecanismos incompatibles entre sí
