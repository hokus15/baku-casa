# SHARED-0004: Financial Entity Semantics

---

## Objetivo

Centralizar la semántica compartida de las entidades económicas y representaciones documentales derivadas reutilizable por múltiples features, para evitar divergencias en la interpretación de importes persistidos, importes derivados, compensaciones y valores efectivos usados en cálculos agregados.

Este documento existe para que las specs consumidoras no tengan que redefinir en cada caso la misma disciplina base para `Accrual`, `Payment`, `Invoice` y demás entidades con semántica monetaria relacionada.

---

## Ámbito de uso

Este shared spec aplica cuando una spec defina entidades económicas fuente o representaciones documentales derivadas que:

- persistan importes monetarios positivos o cero
- representen correcciones mediante entidades compensatorias o de reversión
- calculen importes derivados a partir de una base imponible y porcentajes fiscales
- utilicen importes efectivos (`effective_*`) para agregaciones, balances o reporting

No aplica a:

- master data no económico sin semántica monetaria derivada
- decisiones de persistencia, concurrencia o transporte técnico
- reglas fiscales concretas que pertenezcan a una feature específica

---

## Definiciones

- **Entidad económica o documental derivada**: registro del sistema con semántica monetaria observable, ya sea como hecho económico fuente o como representación documental derivada, como `Accrual`, `Payment` o `Invoice`.
- **Importe persistido**: cantidad monetaria almacenada explícitamente en una entidad con semántica monetaria.
- **Entidad compensatoria o de reversión**: entidad que corrige otra previa mediante una referencia del tipo `reversal_of_*`, sin modificar el registro original.
- **Signo efectivo (`effect_sign`)**: signo algebraico derivado de si la entidad es original (`+1`) o compensatoria/reversa (`-1`).
- **Importe efectivo (`effective_*`)**: importe derivado aplicando `effect_sign` al importe monetario correspondiente para permitir agregaciones netas correctas.

---

## Contenido compartido

Este documento centraliza los siguientes elementos reutilizables:

- la disciplina común de importes monetarios persistidos y no negativos
- la semántica base de compensación mediante entidades nuevas en lugar de edición destructiva
- el uso de `effect_sign` y `effective_*` como contrato común para cálculos netos y reporting

---

## Reglas compartidas

Este shared spec define las siguientes reglas reutilizables:

- Los importes monetarios persistidos en entidades con semántica monetaria deben ser siempre positivos o cero.
- El signo económico o documental neto no debe persistirse como importe negativo; debe derivarse mediante la semántica de compensación o reversión definida por la entidad.
- Toda corrección de una entidad previamente registrada con semántica monetaria debe modelarse mediante una nueva entidad compensatoria o de reversión, nunca alterando silenciosamente el efecto histórico ya reconocido.
- Cuando una entidad con semántica monetaria use una referencia del tipo `reversal_of_*`, su contribución neta debe derivarse mediante `effect_sign`.
- Si la entidad original usa `effect_sign = +1`, la entidad compensatoria o reversa correspondiente debe usar `effect_sign = -1`.
- Los cálculos agregados, balances, reporting y trazabilidad histórica deben apoyarse en importes efectivos (`effective_*`) en lugar de sumas directas de importes persistidos cuando pueda haber compensaciones.
- Cuando una entidad exponga `base_amount`, `vat_rate_percent` y `withholding_rate_percent`, los importes derivados deben seguir la semántica común:
  - `vat_amount = base_amount * vat_rate_percent / 100`
  - `withholding_amount = base_amount * withholding_rate_percent / 100`
  - `gross_amount = base_amount + vat_amount`
  - `net_payable_amount = gross_amount - withholding_amount`
- Las specs consumidoras pueden especializar restricciones de cardinalidad, elegibilidad fiscal, alcance de reversión o límites de corrección, pero no redefinir esta semántica base.

---

## Contrato observable

Cuando este shared spec aplique, las especificaciones consumidoras deben respetar:

- importes persistidos no negativos
- correcciones observables mediante nuevas entidades referenciadas con `reversal_of_*` o semántica equivalente explícita
- disponibilidad de importes efectivos (`effective_*`) para cualquier cálculo neto donde puedan existir compensaciones

Si una entidad expone base y porcentajes fiscales, el contrato observable también debe ser consistente con:

- `vat_amount`
- `withholding_amount`
- `gross_amount`
- `net_payable_amount`

La spec consumidora puede definir nombres adicionales o derivados propios, pero no romper estas fórmulas base ni la disciplina de importes efectivos.

---

## Referencias normativas

Este shared spec puede apoyarse en:

- `docs/system/constitution.md` — secciones `economic_model`, `accounting_invariants`, `monetary_policy` y `percentage_representation`
- ADR-0011 — Monetary and Percentage Representation

---

## Specs consumidoras

Este shared spec puede ser referenciado por:

- docs/specs/features/F-0010-devengos-fuente-unica-de-ingresos-y-gastos.md
- docs/specs/features/F-0011-pagos-asignacion-fifo-y-credito-por-contrato.md
- docs/specs/features/F-0012-facturacion.md
- docs/specs/features/F-0015-reports-fiscales.md

---

## Criterios de adopción

Este shared spec se considera correctamente introducido cuando:

- las specs consumidoras referencian este documento en lugar de repetir la disciplina base de importes positivos, compensaciones y `effective_*`
- las especializaciones locales quedan limitadas a reglas de negocio propias de cada feature
- no existen divergencias incompatibles entre las specs consumidoras respecto a fórmulas derivadas, reversión compensatoria o uso de importes efectivos

---

## Notas de mantenimiento (opcional)

Si una feature introduce una entidad económica nueva, debe reutilizar este shared spec siempre que comparta la misma disciplina de importes positivos, reversión por compensación y agregación mediante importes efectivos.
