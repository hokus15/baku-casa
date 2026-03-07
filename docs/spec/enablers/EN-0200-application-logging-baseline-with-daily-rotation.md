# EN-0200: Application Logging Baseline with Daily Rotation

## Objetivo
Establecer un baseline de logging para la aplicación que permita diagnóstico operativo y análisis técnico fiable, definiendo:

- un **formato estructurado estándar para cada registro**
- un **formato adicional orientado a lectura humana**
- **campos obligatorios**
- **convenciones de logging**
- **persistencia en fichero con rotación diaria**

El sistema de logging debe ser consistente, fácilmente procesable por herramientas automáticas y adecuado para entornos self-hosted.

---

## Descripción

Actualmente la aplicación no dispone de un baseline homogéneo de logging. Esto dificulta el diagnóstico de incidencias, el análisis post-mortem y el soporte operativo.

Este enabler define los requisitos mínimos que debe cumplir el sistema de logging de la aplicación, incluyendo:

- formato estructurado de los registros
- formato alternativo legible por operadores
- campos obligatorios
- convenciones de nomenclatura
- persistencia de logs en fichero
- rotación automática de logs

El objetivo es asegurar que todos los eventos técnicos relevantes queden registrados de forma consistente y que puedan correlacionarse mediante identificadores de ejecución.

Adicionalmente, este enabler debe aplicarse sobre funcionalidades ya desarrolladas para incorporar logging homogéneo en los flujos existentes, incluyendo como mínimo:

- enabler EN-0202
- feature F-0001

---

## Root afectado

- `backend/`

---

## Incluye

### Baseline de logging

Definición de un sistema de logging consistente en toda la aplicación que incluya:

- niveles de log soportados (por ejemplo: DEBUG, INFO, WARNING, ERROR)
- formato estructurado de registros
- formato de registros human friendly
- convenciones de nomenclatura de campos
- persistencia en fichero
- instrumentación del logging en funcionalidades ya implementadas, incluyendo enabler EN-0202 y feature F-0001


---

### Aplicación sobre funcionalidades existentes

El baseline de logging no debe limitarse a nuevas implementaciones. Debe incorporarse también en funcionalidades ya desarrolladas para asegurar trazabilidad operativa y consistencia técnica.

Como parte de este enabler, se debe añadir logging estructurado al menos en:

- flujos del enabler EN-0202
- flujos de la feature F-0001


En estos flujos deben registrarse, como mínimo cuando aplique:

- inicio y fin de operaciones relevantes
- errores técnicos y fallos de validación
- eventos de autenticación relevantes, evitando exponer secretos o datos sensibles en los logs

---

### Formato de los registros

Cada evento de log debe generarse simultáneamente en **dos formatos complementarios**:

1. un fichero de log en **JSON estructurado**, orientado a procesamiento automático
2. un fichero de log **human friendly**, orientado a inspección manual por desarrolladores y operadores

El formato estructurado recomendado es **JSON estructurado**.

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

El fichero **human friendly** debe representar los mismos eventos, pero en un formato de texto claramente legible sin necesidad de herramientas de parsing. Para este enabler, se considera human friendly un formato de una línea por evento, escaneable visualmente y con los datos clave visibles en orden estable, por ejemplo:

- timestamp legible en UTC
- nivel de log claramente destacado
- nombre del servicio o componente
- `correlation_id`
- mensaje principal
- contexto técnico más relevante resumido como pares `clave=valor`

Ejemplo orientativo de línea human friendly:

```text
2026-03-04T21:17:33.482Z INFO baku-backend correlation_id=7c9d8c6b4a7f4c1d9f2e8b7a5c3d2e1f HTTP request completed method=GET path=/contracts status_code=200 duration_ms=32
```

El formato human friendly no debe sacrificar legibilidad con payloads excesivamente verbosos ni incluir secretos, tokens, contraseñas o datos sensibles.

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

- Generación de **dos ficheros de log separados**: uno estructurado en JSON y otro human friendly.
- Ambos ficheros deben registrar el mismo conjunto de eventos relevantes, adaptado a su formato de salida.
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

La salida en JSON y la salida human friendly deben derivarse del mismo evento lógico para evitar divergencias semánticas entre ambos ficheros.

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
