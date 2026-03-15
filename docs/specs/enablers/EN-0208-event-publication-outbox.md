# EN-0208: Event Publication Outbox

---

## Objetivo

Introducir una capacidad de publicación duradera de eventos del dominio mediante outbox pattern para habilitar los flujos definidos por ADR-0010 con garantías de persistencia, reintento y recuperación tras fallo.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- persistencia duradera de eventos del dominio como parte de la misma transacción que el cambio de estado de negocio
- publicación asíncrona y recuperable de eventos mediante un mecanismo desacoplado de los casos de uso del dominio

El enabler afecta principalmente a:

- backend, publicación de eventos, integraciones y automatizaciones que dependan de eventos del dominio

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- event sourcing, rediseño del dominio para ser event-driven o sustitución del modelo transaccional principal del sistema
- definición funcional de los eventos de negocio concretos que pertenezcan a features individuales o redefinición del baseline de observabilidad de EN-0200

---

## Problema que resuelve

ADR-0010 exige un mecanismo de publicación duradera de eventos mediante outbox pattern, pero el sistema todavía no dispone de una capacidad transversal que permita persistir eventos junto con la transacción de negocio, reintentarlos de forma segura y recuperarlos tras un reinicio. Sin este enabler, las features que necesiten publicar eventos con garantías operativas quedarían forzadas a soluciones ad hoc, con riesgo de pérdida de eventos, duplicidades mal gestionadas o acoplamiento indebido entre dominio e infraestructura.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- los cambios de negocio que deban publicar eventos pueden persistirlos de forma duradera dentro de la misma unidad transaccional que el cambio de estado correspondiente
- el sistema puede publicar de forma asíncrona eventos pendientes sin bloquear la transacción principal y con recuperación segura tras fallo o reinicio
- las features futuras que dependan de publicación de eventos, incluyendo automatizaciones supervisadas, pueden apoyarse en una base común coherente con ADR-0010

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- persistencia, servicios de aplicación e infraestructura de publicación de eventos del backend
- features que generen o consuman eventos con entrega duradera, incluyendo como mínimo F-0014 y cualquier flujo posterior que dependa de ADR-0010

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler puede depender de:

- EN-0200
- F-0011

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0010 — Event Publication and Delivery Mechanism
- ADR-0009 — Error Model and Observability

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- el sistema puede persistir eventos pendientes en una estructura de outbox de forma atómica junto con la transacción de negocio que los origina
- existe un mecanismo de publicación desacoplado capaz de recuperar, intentar publicar y marcar como procesados los eventos pendientes según la disciplina definida por ADR-0010
- la capacidad de outbox conserva suficiente información persistida para identificar cada evento, su payload versionado y su estado operativo de publicación
- la publicación reintenta fallos con una política acotada y permite reanudar eventos pendientes tras reinicio sin pérdida silenciosa de eventos
- los fallos de publicación quedan trazados operativamente y no provocan pérdida silenciosa de eventos ya confirmados en la transacción de negocio
- las features que dependan de publicación duradera de eventos pueden apoyarse en esta capacidad común sin implementar mecanismos ad hoc de persistencia y reintento
