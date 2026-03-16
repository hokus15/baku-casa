# F-0004: Datos Económicos de la Propiedad (Adquisición, Venta y Base Fiscal)

---

## Objetivo

Permitir registrar en cada propiedad **0..N apuntes económicos** asociados a su adquisición o transmisión, diferenciando importe real e importe fiscal, categorizados mediante una lista cerrada global, y dejando preparada la base estructural para el cálculo futuro de bases fiscales.

---

## Alcance

- Gestión CRUD de apuntes económicos.
- Asociación exclusiva a una propiedad.
- Validación contra lista cerrada global de categorías.
- Soporte de categorías compartidas entre adquisición y transmisión.
- Persistencia de información necesaria para cálculo futuro de:
  - Base de adquisición.
  - Base de transmisión.
- Determinación estructural de deducibilidad vía categoría.
- Los EconomicEntry no afectan al saldo/deuda del contrato y no participan en el cálculo contable del ledger.

---

## Fuera de alcance

- Cálculo automático de impuestos.
- Cálculo de ganancia/pérdida patrimonial.
- Generación de modelos fiscales.
- Automatización contable.
- Gestión multi-moneda.
- Integración documental (OCR, almacenamiento binario).

---

## Definiciones

- **Propiedad**: activo inmobiliario gestionado en el sistema.
- **Apunte económico**: registro unitario asociado a una propiedad que representa un importe económico vinculado a la adquisición o transmisión.
- **Cantidad real**: importe efectivamente pagado o cobrado.
- **Cantidad fiscal**: valor escriturado o facturado con relevancia tributaria.
- **Adquisición**: operación de entrada del activo en patrimonio.
- **Transmisión**: operación de salida del activo del patrimonio.
- **Categoría**: valor perteneciente a una lista cerrada global del sistema.
- **Categoría deducible**: categoría marcada estructuralmente como deducible a efectos fiscales.
- Estos apuntes (EconomicEntry) NO son eventos del ledger: son master data económica editable usada para cálculo futuro de bases fiscales.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Propiedad
- Apunte económico

---

## Datos principales

La feature gestiona la siguiente información:

### Entidad

### EconomicEntry

**Campos obligatorios**

- `property_id`
- `movement_type`: enum { ACQUISITION, TRANSFER }
- `category`: enum (lista cerrada):
      Adquisición
      Notaría
      Registro
      ITP
      IVA
      Reformas
      Comisiones
      Arquitecto
      Otros
      Otros impuestos
      Venta
      Plusvalía
      No computable
      Tasación
      Subrogación préstamo
- `date`: date
- `amount_real`: decimal positivo
- `amount_fiscal`: decimal positivo

**Campos opcionales**

- `notes`: string
- `document_reference`: string
- `external_id`: string

### Auditoría y soft delete

Esta feature reutiliza el contrato común definido en:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
Los registros eliminados lógicamente no deben mostrarse en consultas normales, pero deben preservarse para trazabilidad histórica.

**Reglas estructurales**

- Los importes son siempre positivos.
- La categoría determina si el apunte es fiscalmente deducible.
- Existe al menos una categoría obligatoria de tipo “precio principal” para:
  - adquisición
  - transmisión

**Relación**

- 1 Propiedad → 0..N EconomicEntry

---

## Capacidades

- Crear apunte económico asociado a una propiedad.
- Editar apunte económico.
- Eliminar apunte económico (soft delete).
- Listar apuntes de una propiedad.
- Filtrar por tipo de movimiento.
- Consultar detalle de un apunte.
- Marcar propiedad como transmitida sin impedir la edición posterior de apuntes.
- Los listados y consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Reglas del dominio

1. Una propiedad puede no tener ningún apunte económico.
2. Cada apunte debe tener `movement_type`, `category`, `date`, `amount_real`, `amount_fiscal`.
3. Los importes deben ser estrictamente positivos o cero.
4. La categoría debe pertenecer a la lista cerrada global.
5. Las categorías pueden ser compartidas entre adquisición y transmisión.
6. Se permiten múltiples apuntes con la misma categoría y tipo.
7. Debe existir al menos una categoría estructural definida como:
   - Precio principal de adquisición.
   - Precio principal de transmisión.
8. La deducibilidad fiscal de un apunte viene determinada exclusivamente por su categoría.
9. Se permite modificar apuntes incluso si la propiedad ya está marcada como transmitida.
10. La eliminación de apuntes debe ser lógica (soft delete).
11. No puede existir un apunte sin propiedad asociada.
12. El diseño debe permitir el cálculo futuro de bases fiscales agregando:
    - Precio principal.
    - Gastos deducibles.
    - Otros ajustes.

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Una propiedad puede no tener ningún apunte económico.
- Cada apunte debe tener `movement_type`, `category`, `date`, `amount_real`, `amount_fiscal`.
- Los importes deben ser estrictamente positivos o cero.

---

## Dependencias

Esta feature puede depender de:

- F-0003

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
- docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- Crear apunte económico asociado a una propiedad.
- Editar apunte económico.
- Eliminar apunte económico (soft delete).

---

