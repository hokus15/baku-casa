# EN-0200: Application Logging Baseline with Daily Rotation

## Objetivo
Establecer un baseline de logging para la aplicación que permita diagnóstico operativo y análisis técnico fiable, definiendo:

- un **formato estructurado estándar para cada registro**
- **campos obligatorios**
- **convenciones de logging**
- **persistencia en fichero con rotación diaria**

El sistema de logging debe ser consistente, fácilmente procesable por herramientas automáticas y adecuado para entornos self-hosted.

---

## Descripción

Actualmente la aplicación no dispone de un baseline homogéneo de logging. Esto dificulta el diagnóstico de incidencias, el análisis post-mortem y el soporte operativo.

Este enabler define los requisitos mínimos que debe cumplir el sistema de logging de la aplicación, incluyendo:

- formato estructurado de los registros
- campos obligatorios
- convenciones de nomenclatura
- persistencia de logs en fichero
- rotación automática de logs

El objetivo es asegurar que todos los eventos técnicos relevantes queden registrados de forma consistente y que puedan correlacionarse mediante identificadores de ejecución.

---

## Root afectado

- `backend/`

---

## Incluye

### Baseline de logging

Definición de un sistema de logging consistente en toda la aplicación que incluya:

- niveles de log soportados (por ejemplo: DEBUG, INFO, WARNING, ERROR)
- formato estructurado de registros
- convenciones de nomenclatura de campos
- persistencia en fichero

---

### Formato de los registros

Cada registro de log debe utilizar un **formato estructurado** que permita su procesamiento automático.

El formato recomendado es **JSON estructurado**.

Cada registro de log debe contener obligatoriamente los siguientes campos:

- `timestamp` — timestamp del evento en **UTC**, utilizando formato **ISO 8601 / RFC3339**
- `level` — nivel del log
- `service_name` — identificador del servicio que genera el log
- `environment` — entorno de ejecución (por ejemplo: `dev`, `test`, `prod`)
- `correlation_id` — identificador de correlación asociado a la ejecución
- `message` — mensaje descriptivo del evento

Además, los registros pueden incluir **campos contextuales opcionales** cuando sea necesario para diagnóstico técnico.

Ejemplos típicos de campos contextuales:

- `method`
- `path`
- `status_code`
- `duration_ms`
- `user_id`
- `property_id`
- `contract_id`
- `error_type`

Los campos contextuales deben añadirse como **campos independientes**, no embebidos dentro del mensaje.

---

### Convenciones de logging

Los registros de log deben seguir las siguientes convenciones:

- Los **mensajes de log deben estar en inglés**.
- Los nombres de campos deben utilizar **snake_case**.
- El campo `message` debe describir el evento ocurrido de forma concisa.
- La información contextual debe incluirse como **campos estructurados adicionales**, no concatenada en el mensaje.

---

### Persistencia y rotación de logs

Los logs deben persistirse en fichero durante la ejecución normal de la aplicación.

El sistema de logging debe cumplir las siguientes condiciones:

- Rotación automática de logs **diariamente a las 00:00 (Europe/Madrid)**.
- Generación de nuevos ficheros de log tras cada rotación.
- Convención de nombres que permita identificar fácilmente la fecha de cada fichero rotado.
- Definición de una política de **retención automática** de logs (por ejemplo número máximo de días o ficheros).

---

## Fuera de alcance

- Sistemas externos de agregación de logs (ELK, Loki, etc.).
- Distributed tracing.
- Sistemas de métricas o alerting.
- Definición de un catálogo completo de eventos de negocio.

---

## Notas de arquitectura

El logging es un **cross-cutting concern** y no debe introducir dependencias técnicas en la capa Domain.

El timestamp de cada registro debe utilizar **UTC** para evitar ambigüedades relacionadas con cambios de zona horaria o horario de verano.

La rotación de ficheros se realiza en **Europe/Madrid** para facilitar la operación y mantenimiento en entornos self-hosted.

Los registros de log deben permitir correlacionar eventos pertenecientes a una misma ejecución mediante el campo `correlation_id`.

---

## Ejemplo de registro de log

```json
{
  "timestamp": "2026-03-04T21:17:33.482Z",
  "level": "INFO",
  "service_name": "baku-backend",
  "environment": "prod",
  "correlation_id": "7c9d8c6b4a7f4c1d9f2e8b7a5c3d2e1f",
  "message": "HTTP request completed",
  "method": "GET",
  "path": "/contracts",
  "status_code": 200,
  "duration_ms": 32
}