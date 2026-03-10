# Research - F-0003 Propiedades y Titularidad

## 1) Total permitido de titularidad

- Decision: El total permitido para la suma de `ownership_percentage` es 100; se acepta suma menor a 100 y se rechaza suma mayor a 100.
- Rationale: Preserva la regla funcional aclarada en spec, permite titularidad parcial y mantiene semantica de porcentaje 0-100 alineada con constitucion y ADR-0011.
- Alternatives considered:
  - Exigir suma exacta 100 en toda operacion: descartado por contradecir la aclaracion funcional.
  - Total configurable por propiedad: descartado por agregar complejidad fuera de alcance.

## 2) Precision y representacion de porcentaje

- Decision: `ownership_percentage` se modela como Decimal en rango 0-100 con precision maxima de 2 decimales.
- Rationale: Cumple constitucion (representacion 0-100), mantiene contrato simple en API y evita ambiguedad de redondeo en MVP1.
- Alternatives considered:
  - Precision de 4 o 6 decimales: descartado por no ser necesario para el alcance actual.
  - Solo enteros: descartado por limitar casos reales de copropiedad.

## 3) Unicidad de titularidad activa por par propiedad-propietario

- Decision: Solo puede existir una titularidad activa por (`property_id`, `owner_id`).
- Rationale: Evita duplicidad logica, simplifica validaciones de suma y mantiene consistencia en consultas activas con soft-delete.
- Alternatives considered:
  - Permitir multiples filas activas por par: descartado por ambiguedad en reglas de negocio.
  - Permitir duplicados con porcentajes distintos: descartado por riesgo de incoherencia en calculos y lectura funcional.

## 4) Campos catastrales derivados

- Decision: `cadastral_construction_value` y `construction_ratio` son campos derivados no editables; `construction_ratio` se considera no aplicable cuando el divisor (`cadastral_value`) es 0 o ausente.
- Rationale: Respeta la especificacion funcional, evita division invalida y mantiene reglas deterministas.
- Alternatives considered:
  - Permitir edicion directa de campos derivados: descartado por contradecir reglas del slice.
  - Forzar `construction_ratio=0` cuando no aplica: descartado por mezclar ausencia de dato con valor real.

## 5) Paginacion y configurabilidad transversal

- Decision: Listados con `page=1`, `page_size=20`, `max_page_size=100`; `page_size` y `max_page_size` configurables de forma transversal para todas las listas.
- Rationale: Cumple ADR-0004 (listas acotadas) y EN-0202 (configuracion centralizada y validada) sin introducir convenciones divergentes.
- Alternatives considered:
  - Valores por defecto menores (10/50): descartado por menor eficiencia operativa en consultas frecuentes.
  - Sin default fijo: descartado por crear variabilidad entre endpoints.

## 6) Contrato temporal y serializacion

- Decision: `timestamps` en ISO-8601 UTC con sufijo `Z`; fechas puras (`acquisition_date`, `transfer_date`) en `YYYY-MM-DD`.
- Rationale: Cumple ADR-0012 y evita ambiguedades entre fecha y datetime en contratos.
- Alternatives considered:
  - Serializar todo como datetime: descartado por perder semantica de campos de fecha pura.
  - Mantener formato "estandar" sin concretar: descartado por no ser testeable.

## 7) Modelo de errores y observabilidad

- Decision: Reutilizar modelo de errores tipificados (`error_code` estable en ingles, `message` en espanol, `correlation_id`) y logging estructurado con baseline EN-0200 sin incluir PII por defecto.
- Rationale: Alinea ADR-0009 y constitucion; mejora trazabilidad operativa sin filtrar datos sensibles.
- Alternatives considered:
  - Errores genericos sin tipado estable: descartado por romper consistencia contractual.
  - Logs con datos fiscales completos para depuracion: descartado por politica de privacidad en observabilidad.

## 8) Dependencias aplicables y alcance

- Decision: Tratar como baseline obligatorio los enablers `EN-0100`, `EN-0202`, `EN-0200`, `EN-0201`, `EN-0300` y la dependencia funcional `F-0002`.
- Rationale: El DAG define estas dependencias directas/transitivas y su aplicabilidad a features futuras.
- Alternatives considered:
  - Ignorar enablers no mencionados en la descripcion funcional: descartado por incumplir regla de baseline acumulado.

## Resultado

No quedan puntos `NEEDS CLARIFICATION` abiertos para F-0003 en este ciclo de planificacion.
