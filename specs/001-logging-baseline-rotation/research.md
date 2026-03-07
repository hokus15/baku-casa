# Research: EN-0200 Application Logging Baseline with Daily Rotation

## Decision 1: Logging estructurado obligatorio con campos minimos constitucionales
- Decision: Mantener como obligatorios `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message` en todos los eventos de log.
- Rationale: `docs/spec/constitution.md` y `ADR-0009` establecen este minimo para trazabilidad y operacion reproducible.
- Alternatives considered:
  - Usar solo mensaje libre en texto: rechazado por baja trazabilidad.
  - Hacer campos opcionales por endpoint: rechazado por romper consistencia operativa.

## Decision 2: Doble salida de logs (JSON + human-friendly)
- Decision: Registrar el mismo evento logico en dos salidas de fichero: JSON estructurado y formato legible humano.
- Rationale: EN-0200 lo exige explicitamente para analisis automatizado y diagnostico manual.
- Alternatives considered:
  - Solo JSON: rechazado por menor ergonomia operativa en inspeccion manual.
  - Solo texto legible: rechazado por peor procesabilidad automatica.

## Decision 3: Rotacion diaria Europe/Madrid con timestamps UTC
- Decision: Rotar ficheros diariamente a las 00:00 Europe/Madrid manteniendo `timestamp` UTC en cada evento.
- Rationale: Constitucion y ADR-0012 separan politica temporal operativa (rotacion) de representacion interna de tiempo (UTC).
- Alternatives considered:
  - Rotacion en UTC: rechazada por desalineacion con criterio operativo explicitado.
  - Timestamps en hora local: rechazada por violar ADR-0012.

## Decision 4: Retencion temporal por dias (default 7) + ficheros activos
- Decision: Aplicar retencion de logs rotados mediante ventana temporal en dias, con valor inicial de 7 dias y posibilidad de configuracion por entorno, manteniendo ficheros activos del dia en curso.
- Rationale: Se requiere comportamiento inicial determinista con ajuste operativo posterior sin cambiar codigo ni redefinir contratos.
- Alternatives considered:
  - Retencion por numero fijo de ficheros: rechazada por acoplar politica operativa al volumen diario de eventos.
  - Valor fijo no configurable: rechazado por rigidez operativa entre entornos.

## Decision 5: Configuracion de logging en perfiles del framework en raiz de backend
- Decision: Definir la configuracion del framework de logging en ficheros dedicados por entorno (`dev`, `test`, `prod`) ubicados en la raiz de `backend/`.
- Rationale: Aclaracion de spec para mantener una integracion simple: la aplicacion solo carga el perfil activo del framework.
- Alternatives considered:
  - Mantener configuracion de logging embebida en codigo: rechazada por acoplamiento y menor mantenibilidad operativa.

## Decision 6: Fallback seguro si falta o es invalido el perfil de logging activo
- Decision: Si el perfil de logging del entorno activo falta o es invalido, aplicar fallback seguro del framework manteniendo baseline minimo obligatorio de logging (sin modo "sin logging") y sin bloquear operacion de la aplicacion.
- Rationale: Mantener desacoplamiento de la aplicacion respecto al framework y permitir configuraciones operativas que reduzcan o desactiven logging.
- Alternatives considered:
  - Mantener fail-fast estricto: rechazado porque acopla disponibilidad de la aplicacion a un artefacto operativo del framework.

## Decision 7: Contrato de fallback por entorno con escritura en consola
- Decision: El fallback de logging se define por entorno con escritura en consola y baseline minimo obligatorio de campos.
- Contrato por entorno:
  - `dev`: salida en consola human-friendly para depuracion local.
  - `test`: salida en consola human-friendly minimalista para aserciones deterministas.
  - `prod`: salida en consola JSON estructurada para ingestabilidad operativa.
- Rationale: Evitar modo "sin logging" y mantener trazabilidad aun cuando falle la carga del perfil principal.
- Alternatives considered:
  - Fallback identico en todos los entornos: rechazado por menor ergonomia en dev/test y menor ingestabilidad en prod.

## Decision 8: Superficie contractual externa sin cambios
- Decision: EN-0200 no modifica contratos HTTP ni eventos publicados.
- Rationale: Item de tipo enabler de observabilidad, alcance transversal interno del backend.
- Alternatives considered:
  - Exponer nuevos endpoints de observabilidad: fuera de alcance del roadmap de EN-0200.

## Decision 9: Impacto documental transversal en features existentes
- Decision: Actualizar las features existentes en `docs/spec/features/` para alinear observabilidad cuando aplique, preservando su alcance funcional.
- Rationale: Aclaracion de spec y regla de consistencia documental del roadmap.
- Alternatives considered:
  - Actualizar solo dependencias directas/transitivas del DAG: rechazado por aclaracion explicita de sesion.
