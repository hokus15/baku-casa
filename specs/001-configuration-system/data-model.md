# Data Model - EN-0202 Configuration System

## Entity: ConfigurationParameterDefinition
- Purpose: Definir contrato normativo de cada clave de configuracion.
- Fields:
  - `key`: identificador estable de la clave.
  - `required`: indica obligatoriedad global.
  - `type_constraint`: regla de tipo esperada.
  - `format_or_range_constraint`: validaciones de formato/rango cuando aplique.
  - `default_value`: valor por defecto explicito (si aplica).
  - `allowed_environments`: entornos en los que la clave puede aplicarse.
  - `description`: descripcion operativa para documentacion.
- Validation Rules:
  - `key` MUST ser unico y estable.
  - Si `required=true`, al menos una fuente debe aportar valor valido.

## Entity: ConfigurationSourceInput
- Purpose: Representar entradas de configuracion por fuente.
- Fields:
  - `source_type`: `environment_variables` | `config_file` | `defaults`.
  - `entries`: pares clave-valor proporcionados por la fuente.
  - `load_context`: entorno objetivo (`dev` | `test` | `prod`).
- Validation Rules:
  - `source_type` MUST pertenecer al conjunto permitido.
  - Entradas deben mapear solo claves conocidas o producir warning de clave no declarada.

## Entity: ResolvedConfigurationProfile
- Purpose: Resultado determinista de composicion para consumo interno.
- Fields:
  - `environment`: entorno efectivo (`dev` | `test` | `prod`).
  - `resolved_values`: mapa final clave-valor tras precedencia.
  - `warnings`: lista de advertencias no bloqueantes.
  - `resolution_trace`: evidencia de fuente ganadora por clave.
- Validation Rules:
  - Precedencia MUST ser `environment variables > config file > defaults`.
  - Debe contener todas las claves requeridas globales con valor valido.

## Entity: ConfigurationValidationIssue
- Purpose: Representar errores de validacion que bloquean arranque.
- Fields:
  - `code`: codigo estable de error de configuracion.
  - `key`: clave afectada.
  - `issue_kind`: `missing` | `type_mismatch` | `format_invalid` | `range_invalid`.
  - `message`: descripcion legible del problema.
- Validation Rules:
  - Cada issue MUST ser tipificado y determinista.
  - El arranque invalido MUST reportar el conjunto completo de issues detectados.

## Relationships
- `ConfigurationParameterDefinition` 1..* -> 0..* `ConfigurationSourceInput` (por `key`).
- `ConfigurationSourceInput` -> `ResolvedConfigurationProfile` (composicion por precedencia).
- `ResolvedConfigurationProfile` -> 0..* `ConfigurationValidationIssue` (si hay fallos bloqueantes).

## State Transitions
- `Unresolved` -> `ResolvedValid` cuando todas las claves requeridas globales son validas.
- `Unresolved` -> `ResolvedInvalid` cuando existen uno o mas `ConfigurationValidationIssue`.
- `ResolvedInvalid` bloquea arranque; `ResolvedValid` habilita arranque.
