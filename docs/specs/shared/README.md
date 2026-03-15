# Shared Specifications

Esta carpeta contiene artefactos **compartidos entre múltiples especificaciones**.

Su propósito es evitar duplicación cuando varias features o enablers necesitan
referenciar exactamente el mismo catálogo, definición o regla funcional.

---

## Cuándo usar `shared`

Un documento debe colocarse en `docs/specs/shared/` **solo si se cumplen todas estas condiciones**:

1. El concepto es utilizado por **múltiples specs**.
2. Las specs necesitan **la misma definición o catálogo**.
3. Se desea mantener **una única fuente de verdad** para evitar divergencias.

Ejemplos típicos de contenido adecuado para `shared`:

- catálogos de dominio reutilizables
- listas cerradas de tipos o estados
- vocabulario funcional común utilizado por varias specs

Ejemplos:

- `SHARED-0001-audit-and-soft-delete.md`
- `SHARED-0002-pagination-contract.md`
- `SHARED-0003-api-response-conventions.md`
- `SHARED-0004-financial-entity-semantics.md`
- `SHARED-0005-idempotency-contract.md`

---

## Cuándo **no** usar `shared`

No debe usarse esta carpeta para:

- reglas globales del sistema  
  → usar `docs/system/constitution.md`

- decisiones técnicas o arquitectónicas  
  → usar `docs/decisions/adr/`

- comportamiento específico de una feature  
  → definirlo dentro de `docs/specs/features/`

- capacidades técnicas del sistema  
  → definirlas en `docs/specs/enablers/`

---

## Regla de extracción

Si una definición aparece en **una sola spec**, debe permanecer dentro de esa spec.

Solo debe moverse a `shared` cuando:

- al menos **dos especificaciones** necesiten usar la misma definición, y
- mantenerla duplicada pueda generar inconsistencias.

