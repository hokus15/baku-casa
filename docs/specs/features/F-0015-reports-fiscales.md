# F-0015: Reports Fiscales

---

## Objetivo

Generar resúmenes fiscales por propietario y periodo utilizando los `Accrual` como fuente única de datos, tomando como referencia la **fecha de devengo (`accrual_date`)**.

Inicialmente se soportan:

- Informe anual de IRPF.
- Modelo 303 (IVA trimestral).

El sistema debe quedar abierto para incorporar nuevos informes fiscales en el futuro.

---

## Alcance

Esta feature cubre:

- Generar informe IRPF por propietario y año.
- Generar modelo 303 por trimestre.
- Exportar resultados en formato estructurado.

---

## Fuera de alcance

- Presentación automática ante AEAT.
- Gestión de fraccionamientos o pagos.
- Gestión de otros modelos (111, 115, 390, etc.).
- Validación avanzada de coherencia tributaria.
- Ajustes por pagos reales (criterio de caja).

---

## Definiciones

- **Periodo fiscal**: intervalo temporal cerrado para el que se calcula un informe.
- **IRPF**: resumen anual de ingresos y gastos deducibles atribuibles a un propietario.
- **Modelo 303**: declaración trimestral de IVA.
- **Propietario**: titular de una propiedad con un ratio de participación.
- **Ratio de propiedad**: porcentaje de titularidad aplicado proporcionalmente cuando proceda.
- **Devengo fiscalmente relevante**: `Accrual` cuya `accrual_date` cae dentro del periodo fiscal, considerando compensaciones mediante importes efectivos conforme a docs/specs/shared/SHARED-0004-financial-entity-semantics.md

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Periodo fiscal
- IRPF
- Modelo 303

---

## Datos principales

La feature gestiona la siguiente información:

### Fuente de datos

- Los informes se construyen exclusivamente a partir de `Accrual`.
- Se consideran únicamente devengos con `accrual_date` dentro del periodo solicitado, agregados usando importes efectivos (`effective_*`) conforme a docs/specs/shared/SHARED-0004-financial-entity-semantics.md

No se utilizan pagos para cálculo fiscal.

---

### IRPF

### Alcance

- Informe anual por propietario y ejercicio natural (1 enero – 31 diciembre).
- Si una propiedad tiene varios propietarios:
  - Se genera el informe solo para el propietario solicitado.
  - Se aplica el `ratio de propiedad` a las cantidades que requieran atribución proporcional.

### Criterios de cálculo

- Ingresos:
  - `Accrual.type = INCOME`
  - `payer = TENANT`
- Gastos deducibles:
  - `Accrual.type = EXPENSE`
  - `payer = OWNER`
  - `category` marcada como deducible
- Las cantidades se toman sobre:
  - `base_amount`
  - No se incluyen pagos ni cobros reales.
- Gastos deducibles IRPF: solo `Accrual.type = EXPENSE` con `payer = OWNER`.
- Los `EXPENSE` con `payer = TENANT` se consideran traslados y NO son deducibles por el propietario por defecto.

### Reglas de negocio IRPF

1. El informe debe generarse para un único propietario por solicitud.
2. El ratio de propiedad se aplica a:
   - ingresos
   - gastos deducibles
   salvo que la categoría indique tratamiento no proporcional (extensible).
3. No se incluyen devengos con `payer = TENANT` tipo gasto.
4. Los devengos se agregan considerando compensaciones mediante importes efectivos (`effective_*`) conforme a docs/specs/shared/SHARED-0004-financial-entity-semantics.md
5. El resultado es un resumen estructurado exportable en formatos adecuados para consulta e intercambio.
6. Si un devengo tiene reverso total, su contribución fiscal neta es 0.
7. Los cálculos fiscales deben usar siempre importes efectivos (`effective_*`) conforme a docs/specs/shared/SHARED-0004-financial-entity-semantics.md

---

### Modelo 303 (IVA)

### Alcance

- El 303 se genera por propietario (sujeto pasivo) y trimestre, consolidando todas las propiedades atribuibles a ese propietario.
- Periodicidad trimestral:
  - 1T: enero–marzo
  - 2T: abril–junio
  - 3T: julio–septiembre
  - 4T: octubre–diciembre
- Solo permitido si la propiedad tiene:
  - Un único propietario al 100%.
  - Puede ser persona física, jurídica o ESPJ (atribución de bienes).

### Criterios de cálculo
- Se agregan importes efectivos de devengos.
- Se consideran solo devengos no completamente revertidos.
- No se utilizan pagos.
- IVA repercutido:
  - `Accrual.type = INCOME`
  - `vat_rate_percent > 0`
- IVA soportado:
  - `Accrual.type = EXPENSE`
  - `vat_rate_percent > 0`
- Base imponible y cuotas se calculan desde:
  - `base_amount`
  - `vat_amount` (derivado)

### Reglas de negocio Modelo 303

1. Solo puede generarse si existe un único propietario al 100%.
2. El periodo debe corresponder a un trimestre natural iniciado en enero.
3. Se consideran devengos con `accrual_date` dentro del trimestre.
4. Los devengos se agregan considerando compensaciones mediante importes efectivos (`effective_*`) conforme a docs/specs/shared/SHARED-0004-financial-entity-semantics.md
5. El sistema debe generar el fichero importable compatible con la AEAT.
6. No se gestionan compensaciones intertrimestrales en esta versión.
7. No se gestionan regímenes especiales de IVA (extensible).
8. Si un devengo tiene reverso total, su contribución fiscal neta es 0.
9. Los cálculos fiscales deben usar siempre importes efectivos (effective_*) conforme a docs/specs/shared/SHARED-0004-financial-entity-semantics.md

---

## Capacidades

- Generar informe IRPF por propietario y año.
- Generar modelo 303 por trimestre.
- Exportar resultados en formato estructurado.
- Generar fichero compatible con AEAT para modelo 303.

---

## Reglas del dominio

- Los informes se construyen exclusivamente a partir de `Accrual`.
- Se consideran únicamente devengos con `accrual_date` dentro del periodo solicitado y los cálculos deben usar importes efectivos (`effective_*`) conforme a docs/specs/shared/SHARED-0004-financial-entity-semantics.md
- En IRPF, el informe se genera para un único propietario por solicitud y aplica el ratio de propiedad cuando corresponda.
- En IRPF, solo son deducibles por defecto los `Accrual.type = EXPENSE` con `payer = OWNER`; los `EXPENSE` con `payer = TENANT` se consideran traslados y no son deducibles por defecto.
- En Modelo 303, solo puede generarse el informe si existe un único propietario al 100% y el periodo corresponde a un trimestre natural.
- En Modelo 303, el sistema debe generar un fichero importable compatible con la AEAT.

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Generar informe IRPF por propietario y año.
- Generar modelo 303 por trimestre.
- Exportar resultados en formato estructurado.

---

## Dependencias

Esta feature puede depender de:

- F-0010

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0004-financial-entity-semantics.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- Generar informe IRPF por propietario y año.
- Generar modelo 303 por trimestre.
- Exportar resultados en formato estructurado.
