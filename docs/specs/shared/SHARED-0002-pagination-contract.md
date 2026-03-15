# SHARED-0002: Pagination Contract

---

## Objetivo

Centralizar la semántica compartida de paginación reutilizable por múltiples features, para evitar divergencias en listados, búsquedas y demás endpoints de colección.

Este documento existe para que las specs consumidoras no tengan que redefinir la misma disciplina base de paginación en cada caso.

---

## Ámbito de uso

Este shared spec aplica cuando una spec defina:

- listados
- búsquedas
- consultas de colección
- cualquier endpoint que devuelva subconjuntos navegables de una colección

No aplica a endpoints de detalle, acciones puntuales ni operaciones que no expongan una colección observable.

---

## Definiciones

- **Consulta de colección**: operación que devuelve cero o más elementos homogéneos de una colección.
- **Paginación**: partición determinista del resultado de una colección en páginas navegables.
- **`page`**: índice lógico de página solicitado por el consumidor.
- **`page_size`**: número máximo de elementos devueltos en una página.
- **`max_page_size`**: límite superior permitido para `page_size`.

---

## Contenido compartido

Este documento centraliza los siguientes elementos reutilizables:

- la obligación de paginar toda consulta de colección
- la resolución centralizada de valores por defecto y límites de paginación
- el contrato observable mínimo que deben cumplir los listados y búsquedas

---

## Reglas compartidas

Este shared spec define las siguientes reglas reutilizables:

- Toda consulta de colección debe usar paginación obligatoria.
- No deben existir listados sin acotar ni respuestas que devuelvan colecciones completas por defecto.
- Los parámetros base de paginación deben resolverse mediante el configuration system definido en EN-0202.
- La precedencia de resolución de configuración debe ser `environment variables > config file > defaults`.
- Los valores por defecto y límites máximos de paginación no deben definirse mediante constantes hardcoded en adapters, servicios de aplicación ni repositorios.
- Debe existir una única fuente de verdad para `page`, `page_size` y `max_page_size`.
- Las specs consumidoras pueden añadir filtros, ordenaciones o restricciones propias, pero no redefinir la semántica base de paginación aquí establecida.

---

## Contrato observable

Cuando este shared spec aplique, las especificaciones consumidoras deben respetar:

- soporte para solicitar subconjuntos paginados de la colección
- un comportamiento determinista respecto a qué elementos pertenecen a cada página
- uso de los parámetros base `page` y `page_size`, salvo que la spec consumidora declare explícitamente una especialización compatible
- uso de valores por defecto y límites resueltos desde configuración central cuando el consumidor no los informe

La forma exacta de los metadatos de respuesta puede especializarse en la spec consumidora o en el contrato del adapter correspondiente, siempre sin romper esta disciplina base.

---

## Referencias normativas

Este shared spec puede apoyarse en:

- `docs/system/constitution.md` — sección `pagination`
- EN-0202 — Configuration System

---

## Specs consumidoras

Este shared spec puede ser referenciado por:

- docs/specs/features/F-0001-acceso-y-autenticacion-operador.md
- docs/specs/features/F-0002-propietarios-sujetos-fiscales.md
- docs/specs/features/F-0003-propiedades-y-titularidad.md
- docs/specs/features/F-0004-datos-economicos-de-la-propiedad-adquisicion-venta-y-base-fiscal.md
- docs/specs/features/F-0005-gastos-recurrentes-de-la-propiedad-master-data.md
- docs/specs/features/F-0006-contratos-estructura-base.md
- docs/specs/features/F-0007-historico-de-rentas-master-data.md
- docs/specs/features/F-0008-clausulas-de-actualizacion-de-renta-master-data.md
- docs/specs/features/F-0009-clausulas-de-asignacion-de-gastos-recurrentes-de-la-propiedad.md
- docs/specs/features/F-0011-pagos-asignacion-fifo-y-credito-por-contrato.md
- docs/specs/features/F-0012-facturacion.md
- docs/specs/features/F-0013-tareas.md

---

## Criterios de adopción

Este shared spec se considera correctamente introducido cuando:

- las specs consumidoras referencian este documento en lugar de repetir el contrato transversal completo de paginación
- cualquier excepción observable queda declarada explícitamente en la spec consumidora
- no existen divergencias incompatibles entre las specs consumidoras respecto a parámetros base, precedencia de configuración o límites hardcoded

---

## Notas de mantenimiento (opcional)

Si una spec necesita restricciones adicionales de paginación, filtrado o ordenación, debe declararlas como especialización local sobre este shared spec, no redefinir silenciosamente la disciplina común.
