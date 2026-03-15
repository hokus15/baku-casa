# SHARED-0003: API Response Conventions

---

## Objetivo

Centralizar las convenciones compartidas de serialización y respuesta de la API reutilizables por múltiples features y enablers, para evitar divergencias en nombres de campos, representación temporal y exposición de valores opcionales.

Este documento existe para que las specs consumidoras no tengan que redefinir las mismas convenciones base de respuesta en cada caso.

---

## Ámbito de uso

Este shared spec aplica cuando una spec defina:

- respuestas JSON expuestas por la API
- DTOs o payloads observables por clientes externos
- errores estructurados expuestos por adapters HTTP o equivalentes

No aplica a:

- modelos internos de dominio
- modelos ORM o persistencia
- eventos internos no expuestos como contrato de respuesta a clientes

---

## Definiciones

- **Respuesta de API**: payload observable devuelto por un adapter externo del sistema.
- **Campo opcional omitido**: campo cuyo valor es `null` en el modelo interno y por tanto no se incluye en la respuesta serializada.
- **Fecha-hora**: instante temporal con zona horaria explícita representado en formato ISO 8601 UTC.
- **Fecha de calendario**: valor de fecha sin hora representado en formato `YYYY-MM-DD`.

---

## Contenido compartido

Este documento centraliza los siguientes elementos reutilizables:

- la convención base de serialización JSON para respuestas de la API
- la representación observable de fechas, horas y campos opcionales
- la estructura mínima esperable para respuestas de error

---

## Reglas compartidas

Este shared spec define las siguientes reglas reutilizables:

- Las respuestas de la API deben usar JSON como formato de intercambio.
- Las claves JSON expuestas por la API deben usar `snake_case`.
- Los campos con valor `null` no deben incluirse en la respuesta serializada.
- Todas las fechas y horas expuestas por la API deben representarse en formato ISO 8601 y corresponder a instantes almacenados en UTC.
- Las fechas sin componente horaria deben representarse en formato `YYYY-MM-DD`.
- Las respuestas de error deben ser estructuradas e incluir al menos un código de error y un mensaje legible.
- Las specs consumidoras pueden añadir campos, snapshots o metadatos propios, pero no romper estas convenciones base de serialización.

---

## Contrato observable

Cuando este shared spec aplique, las especificaciones consumidoras deben respetar:

- nombres de campos observables en `snake_case`
- ausencia de campos opcionales serializados como `null`
- representación consistente de timestamps como valores ISO 8601 UTC y de fechas puras como `YYYY-MM-DD`

Para errores estructurados, el contrato observable mínimo debe permitir identificar:

- `error_code`
- `message`

La spec consumidora puede especializar campos adicionales de error o metadatos de respuesta si lo necesita.

---

## Referencias normativas

Este shared spec puede apoyarse en:

- `docs/system/constitution.md` — secciones `time_policy` y `api_contracts`
- `docs/system/conventions.md` — secciones `Convenciones de API`, `Convenciones de tiempo` y `Convenciones de errores`

---

## Specs consumidoras

Este shared spec puede ser referenciado por:

- docs/specs/features/F-0001-acceso-y-autenticacion-operador.md
- docs/specs/features/F-0002-propietarios-sujetos-fiscales.md
- docs/specs/features/F-0003-propiedades-y-titularidad.md
- docs/specs/features/F-0004-datos-economicos-de-la-propiedad-adquisicion-venta-y-base-fiscal.md
- docs/specs/features/F-0011-pagos-asignacion-fifo-y-credito-por-contrato.md
- docs/specs/features/F-0012-facturacion.md

---

## Criterios de adopción

Este shared spec se considera correctamente introducido cuando:

- las specs consumidoras referencian este documento en lugar de repetir reglas base de serialización JSON, timestamps o campos `null`
- cualquier excepción observable queda declarada explícitamente en la spec consumidora
- no existen divergencias incompatibles entre las specs consumidoras respecto a `snake_case`, representación temporal o forma mínima de errores

---

## Notas de mantenimiento (opcional)

Si una spec necesita un contrato de respuesta más específico, debe especializar este shared spec sin redefinir silenciosamente las convenciones base de serialización.
