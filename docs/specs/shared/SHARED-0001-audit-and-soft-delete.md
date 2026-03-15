# SHARED-0001: Audit and Soft Delete

---

## Objetivo

Centralizar la semántica compartida de auditoría y soft delete reutilizable por múltiples features y enablers, para evitar divergencias en campos, comportamiento observable y reglas de borrado lógico.

Este documento existe para que las specs consumidoras no tengan que redefinir la misma disciplina de auditoría y eliminación lógica en cada caso.

---

## Ámbito de uso

Este shared spec aplica cuando una spec defina entidades persistidas que deban:

- mantener trazabilidad de creación y modificación
- permitir borrado lógico en lugar de eliminación física
- exponer un comportamiento consistente respecto a registros eliminados

No debe usarse para eventos económicos append-only que, por reglas del dominio, no admiten soft delete.

---

## Definiciones

- **Auditoría**: metadatos que permiten conocer cuándo y por quién fue creada, actualizada o marcada como eliminada una entidad.
- **Soft delete**: eliminación lógica que conserva el registro persistido y lo excluye de las consultas normales.
- **Registro activo**: entidad no marcada como eliminada, es decir, con `deleted_at = null`.

---

## Contenido compartido

Este documento centraliza los siguientes elementos reutilizables:

- el conjunto estándar de campos de auditoría para entidades persistidas mutables
- la semántica común de soft delete
- el comportamiento observable por defecto de listados, detalles y relaciones frente a registros eliminados

---

## Reglas compartidas

Este shared spec define las siguientes reglas reutilizables:

- Toda entidad mutable que use este shared spec debe incluir `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at` y `deleted_by`.
- `created_at` y `created_by` deben registrarse en la creación; `updated_at` y `updated_by` deben reflejar la última modificación efectiva.
- Si una entidad admite eliminación lógica, el borrado debe implementarse mediante soft delete y no mediante eliminación física.
- Un soft delete debe registrar `deleted_at` y, cuando el modelo lo soporte, `deleted_by`.
- Los registros marcados como eliminados no deben aparecer en consultas normales, listados ni relaciones activas salvo que la spec consumidora declare explícitamente una excepción observable.
- La restauración o inclusión explícita de registros eliminados solo puede existir si la spec consumidora la define de forma expresa.
- Las reglas de cascada, si existen, deben declararse en la spec consumidora; este documento no impone cascada automática por defecto.

---

## Contrato observable

Cuando este shared spec aplique, las especificaciones consumidoras deben respetar:

- un contrato estable de campos de auditoría con los nombres `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at` y `deleted_by`
- la exclusión por defecto de registros eliminados en consultas normales
- la necesidad de declarar explícitamente cualquier excepción, como `include_deleted`, restauración, cascada de borrado o exposición parcial de registros eliminados

---

## Referencias normativas

Este shared spec puede apoyarse en:

- `docs/system/constitution.md` — secciones `audit_fields` y `soft_delete`
- ADR-0009 — Error Model and Observability

---

## Specs consumidoras

Este shared spec puede ser referenciado por:

- docs/specs/features/F-0002-propietarios-sujetos-fiscales.md
- docs/specs/features/F-0003-propiedades-y-titularidad.md
- docs/specs/features/F-0004-datos-economicos-de-la-propiedad-adquisicion-venta-y-base-fiscal.md
- docs/specs/features/F-0005-gastos-recurrentes-de-la-propiedad-master-data.md
- docs/specs/features/F-0006-contratos-estructura-base.md
- docs/specs/features/F-0008-clausulas-de-actualizacion-de-renta-master-data.md
- docs/specs/features/F-0009-clausulas-de-asignacion-de-gastos-recurrentes-de-la-propiedad.md
- docs/specs/features/F-0013-tareas.md

---

## Criterios de adopción

Este shared spec se considera correctamente introducido cuando:

- las specs consumidoras referencian este documento en lugar de redefinir el contrato estándar completo de auditoría y soft delete
- cualquier excepción al comportamiento por defecto queda declarada en la spec consumidora de forma explícita
- no existen divergencias incompatibles entre las specs consumidoras respecto a nombres de campos o semántica básica de borrado lógico

---

## Notas de mantenimiento (opcional)

Si una spec necesita un comportamiento especial de auditoría o borrado lógico, debe declararlo como especialización local sobre este shared spec, no modificar silenciosamente la semántica base.
