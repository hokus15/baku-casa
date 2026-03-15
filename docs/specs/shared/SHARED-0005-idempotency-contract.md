# SHARED-0005: Idempotency Contract

---

## Objetivo

Centralizar la semántica compartida de idempotencia reutilizable por múltiples features, para evitar divergencias en cómo se identifica una misma operación lógica, cómo se comporta el sistema ante reintentos y cómo se rechazan reutilizaciones incompatibles de una misma identidad.

Este documento existe para que las specs consumidoras no tengan que redefinir en cada caso la misma disciplina base de protección frente a duplicados.

---

## Ámbito de uso

Este shared spec aplica cuando una spec defina operaciones que:

- puedan reintentarse por cliente, automatización o proceso interno
- creen o propongan efectos persistentes que no deban duplicarse
- usen una clave explícita como `idempotency_key` o `automation_key`, o una identidad lógica equivalente

No aplica a:

- validaciones de unicidad puramente de negocio no relacionadas con reintentos
- deduplicación de lectura o consultas sin efecto persistente
- detalles técnicos de implementación del enabler EN-0209

---

## Definiciones

- **Operación lógica**: intento de negocio que, aunque pueda recibirse varias veces, debe producir como máximo un único efecto persistente válido.
- **Identidad de idempotencia**: valor o criterio estable que permite reconocer que dos intentos corresponden a la misma operación lógica.
- **Reintento válido**: nueva recepción de la misma operación lógica con la misma identidad y parámetros materialmente equivalentes.
- **Reutilización incompatible**: uso de la misma identidad de idempotencia con parámetros materialmente distintos a los del intento original.

---

## Contenido compartido

Este documento centraliza los siguientes elementos reutilizables:

- la obligación de definir explícitamente la identidad de una operación lógica protegida
- el comportamiento esperado del sistema ante reintentos válidos
- la respuesta obligatoria ante reutilizaciones incompatibles de una misma identidad

---

## Reglas compartidas

Este shared spec define las siguientes reglas reutilizables:

- Toda operación protegida debe definir explícitamente qué identifica una misma operación lógica.
- La identidad de idempotencia puede expresarse mediante una clave explícita, una restricción determinista o un fingerprint canónico, siempre que la spec consumidora lo declare con claridad.
- Si el sistema recibe un reintento válido de la misma operación lógica, debe devolver el resultado previamente creado o responder de forma determinista como duplicado, sin crear un nuevo efecto persistente.
- Una misma identidad de idempotencia no debe crear más de un efecto persistente material.
- Si la misma identidad se reutiliza con parámetros materialmente distintos, la operación debe rechazarse de forma determinista.
- Las specs consumidoras pueden especializar el ámbito de unicidad, el nombre de la clave o la forma del resultado reutilizado, pero no romper esta disciplina base.

---

## Contrato observable

Cuando este shared spec aplique, las especificaciones consumidoras deben respetar:

- existencia de una identidad de idempotencia explícita o determinable
- seguridad ante reintentos de la misma operación lógica
- rechazo determinista cuando la misma identidad se reutiliza con parámetros incompatibles

La spec consumidora debe declarar además, cuando aplique:

- el nombre de la clave (`idempotency_key`, `automation_key` u otra)
- el alcance de unicidad de esa identidad
- qué resultado observable se reutiliza o devuelve ante un reintento válido

---

## Referencias normativas

Este shared spec puede apoyarse en:

- `docs/system/constitution.md` — sección `idempotency`
- EN-0209 — Idempotency and Duplicate Operation Protection
- ADR-0014 — Idempotent Operations and Duplicate Protection

---

## Specs consumidoras

Este shared spec puede ser referenciado por:

- docs/specs/features/F-0010-devengos-fuente-unica-de-ingresos-y-gastos.md
- docs/specs/features/F-0011-pagos-asignacion-fifo-y-credito-por-contrato.md
- docs/specs/features/F-0013-tareas.md
- docs/specs/features/F-0014-automatizacion-creacion-de-tareas.md

---

## Criterios de adopción

Este shared spec se considera correctamente introducido cuando:

- las specs consumidoras referencian este documento en lugar de repetir la disciplina base de reintento seguro e identidad lógica
- cada spec consumidora declara solo su especialización local de identidad, alcance o payload material
- no existen divergencias incompatibles entre specs consumidoras respecto a reintentos válidos, reutilización incompatible o duplicados persistentes

---

## Notas de mantenimiento (opcional)

Si una feature necesita una identidad específica distinta de `idempotency_key`, debe declararla como especialización local sobre este shared spec, no redefinir silenciosamente el comportamiento base de idempotencia.
