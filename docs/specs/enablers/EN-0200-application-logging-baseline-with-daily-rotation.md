# EN-0200: Application Logging Baseline with Daily Rotation

---

## Objetivo

Establecer un baseline de logging para la aplicación que permita diagnóstico operativo y análisis técnico fiable mediante un formato estructurado consistente, una salida adicional legible por operadores y persistencia en fichero con rotación diaria.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- observabilidad técnica homogénea en la aplicación
- persistencia y rotación diaria de logs con criterios consistentes entre entornos

El enabler afecta principalmente a:

- backend, observabilidad y logging de funcionalidades ya existentes y futuras

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- sistemas externos de agregación de logs, distributed tracing o plataformas de métricas y alerting
- definición de un catálogo completo de eventos de negocio o cambios funcionales en los casos de uso existentes

---

## Problema que resuelve

Actualmente la aplicación no dispone de un baseline homogéneo de logging. Esto dificulta el diagnóstico de incidencias, el análisis post-mortem y el soporte operativo. Sin un formato consistente, campos obligatorios y correlación estable entre eventos, los flujos ya implementados y los que se incorporen en el futuro carecen de trazabilidad operativa fiable.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- los eventos técnicos relevantes quedan registrados de forma consistente en formatos adecuados tanto para procesamiento automático como para inspección manual
- los registros incluyen un baseline mínimo común de campos obligatorios y permiten correlacionar eventos pertenecientes a una misma ejecución
- el sistema conserva logs en fichero con rotación diaria y comportamiento seguro por entorno incluso cuando la configuración del logging no puede cargarse

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- observabilidad operativa y diagnóstico técnico del backend
- trazabilidad de flujos ya implementados, incluyendo como mínimo EN-0202 y F-0001

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

- ADR-0009 — Error Model and Observability
- ADR-0013 — Configuration System

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- la aplicación genera logs con un baseline mínimo consistente, incluyendo como mínimo `timestamp`, `level`, `service_name`, `correlation_id` y `message`
- cada evento relevante queda disponible tanto en un formato estructurado procesable como en un formato human-friendly para inspección manual
- los logs se persisten en fichero con rotación diaria a las 00:00 Europe/Madrid y política de retención configurable por entorno
- las funcionalidades ya implementadas incluidas en el alcance del enabler disponen de trazabilidad operativa homogénea
- si la configuración de logging del entorno activo no puede cargarse, la aplicación mantiene un fallback seguro y no queda sin logging
