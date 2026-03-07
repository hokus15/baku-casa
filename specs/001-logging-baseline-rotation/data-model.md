# Data Model: EN-0200 Application Logging Baseline with Daily Rotation

## Overview
EN-0200 no introduce entidades de dominio ni un modelo de datos de negocio nuevo.
Este artefacto describe unicamente el **artefacto de configuracion del framework de
logging** por entorno para mantener el plan simple y sin capas adicionales.

## Configuration Artifact

### Logging Framework Configuration File (per environment)
- Purpose: Definir la configuracion del framework de logging para cada entorno (`dev`,
  `test`, `prod`) en ficheros separados ubicados en la raiz de `backend/`.
- Scope:
  - Configuracion propia del framework de logging.
  - Externa al codigo de aplicacion y no embebida en modulos.
  - Cargada por la aplicacion en startup mediante bootstrap del framework.

### Required capability groups (implementation-agnostic)
- Salidas de logging:
  - salida estructurada (machine-readable)
  - salida human-friendly (operator-readable)
- Contexto y formato:
  - campos obligatorios en cada evento (`timestamp`, `level`, `service_name`,
    `correlation_id`, `message`)
  - contexto adicional como campos estructurados
- Rotacion:
  - corte diario a las 00:00 (Europe/Madrid)
- Retencion:
  - politica basada en dias
  - valor inicial: 7 dias
  - configurable por entorno
  - preserva ficheros activos del dia en curso

## Validation Rules
- Debe existir un esquema de resolucion de perfil de logging para el entorno activo.
- Si el fichero falta, no puede cargarse o es invalido, se aplica fallback seguro del framework manteniendo baseline minimo obligatorio de logging (sin modo "sin logging") y sin bloquear la aplicacion.
- La configuracion debe permitir operar sin cambios de contrato HTTP/eventos.

## Notes
- El detalle de sintaxis del fichero depende del framework de logging elegido y queda
  fuera de este artefacto.
- EN-0200 define capacidad de observabilidad, no una arquitectura adicional en la capa
  de aplicacion.
