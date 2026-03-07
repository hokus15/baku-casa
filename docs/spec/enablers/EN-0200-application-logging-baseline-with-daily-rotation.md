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

- EN-0202
- F-0001

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
- definición de configuración específica del framework de logging en ficheros en la raíz de `backend/`
- definición de perfiles de logging por entorno (`dev`, `test`, `prod`) en esos artefactos del framework
- instrumentación del logging en funcionalidades ya implementadas, incluyendo EN-0202 y F-0001


---

### Aplicación sobre funcionalidades existentes

El baseline de logging no debe limitarse a nuevas implementaciones. Debe incorporarse también en funcionalidades ya desarrolladas para asegurar trazabilidad operativa y consistencia técnica.

Además del impacto técnico en la implementación, este enabler debe sincronizarse a nivel documental con todas las features existentes en `docs/spec/features/` para unificar criterios de observabilidad.

Como parte de este enabler, se debe añadir logging estructurado al menos en:

- flujos de EN-0202
- flujos de F-0001


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

### Configuración de logging

La configuración de logging debe definirse en **ficheros específicos del framework de logging** ubicados en la raíz de `backend/` (por ejemplo `logging.dev.ini`, `logging.test.ini`, `logging.prod.ini`).

La organización por entorno debe realizarse mediante un **fichero dedicado distinto para cada entorno activo**, al menos para `dev`, `test` y `prod`, mantenido como configuración externa del framework.

Como parte de este enabler se debe definir en los ficheros del framework de logging, al menos por entorno:

- activación y nivel de logging
- rutas o nombres de los dos ficheros de salida
- formato de salida asociado a cada fichero
- política de rotación diaria
- política de retención

Ejemplo de referencia para una implementación estándar: usar `logging` de Python con
`logging.config.fileConfig`, dos `formatters` (JSON y human-friendly), dos `handlers`
de fichero y rotación diaria mediante `logging.handlers.TimedRotatingFileHandler`.

La solución debe permitir que el comportamiento de logging y la retención puedan configurarse por entorno sin modificar código de la aplicación.

La configuración del framework de logging no debe quedar embebida en código y puede reducir la verbosidad mediante los propios perfiles del framework, pero siempre preservando el baseline mínimo obligatorio de logging.

Si el fichero de logging correspondiente al entorno activo no existe, no puede cargarse o contiene una configuración inválida, la aplicación debe aplicar un fallback seguro del framework que mantenga el baseline mínimo obligatorio de logging (timestamp UTC, level, service_name, correlation_id, message) y continuar operativa. No se admite fallback equivalente a "sin logging".

Contrato de fallback por entorno (escritura en consola):

- `dev`: salida por consola en formato human-friendly.
- `test`: salida por consola en formato human-friendly minimalista para aserciones.
- `prod`: salida por consola en formato JSON estructurado.

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
- Política de **retención automática** basada en días para logs rotados, con valor inicial de **7 días** y configuración por entorno, además de conservar los ficheros activos del día en curso.

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
