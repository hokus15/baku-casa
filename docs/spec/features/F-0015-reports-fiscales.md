# F-0015: Reports Fiscales

## Objetivo

Generar resúmenes fiscales por propietario y periodo utilizando los `Accrual` como fuente única de datos, tomando como referencia la **fecha de devengo (`accrual_date`)**.

Inicialmente se soportan:

- Informe anual de IRPF.
- Modelo 303 (IVA trimestral).

El sistema debe quedar abierto para incorporar nuevos informes fiscales en el futuro.

---

## Definiciones

- **Periodo fiscal**: intervalo temporal cerrado para el que se calcula un informe.
- **IRPF**: resumen anual de ingresos y gastos deducibles atribuibles a un propietario.
- **Modelo 303**: declaración trimestral de IVA.
- **Propietario**: titular de una propiedad con un ratio de participación.
- **Ratio de propiedad**: porcentaje de titularidad aplicado proporcionalmente cuando proceda.
- **Devengo fiscalmente relevante**: `Accrual` cuya `accrual_date` cae dentro del periodo fiscal, considerando compensaciones (`reversal_of_accrual_id`) mediante importes efectivos.

---

## Fuente de datos

- Los informes se construyen exclusivamente a partir de `Accrual`.
- Se consideran únicamente devengos con `accrual_date` dentro del periodo solicitado, agregados usando importes efectivos (`effective_*`) para reflejar compensaciones.
- Los importes se agregan usando los importes efectivos (effective_*) para considerar compensaciones.

No se utilizan pagos para cálculo fiscal.

---

## IRPF

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
4. No se incluyen devengos considerando compensaciones (`reversal_of_*`) mediante importes efectivos (`effective_*`)
5. El resultado es un resumen estructurado exportable (JSON/PDF en futuras iteraciones).
7. Si un devengo tiene reverso total, su contribución fiscal neta es 0.
8. Los cálculos fiscales deben usar siempre importes efectivos (effective_*).

---

## Modelo 303 (IVA)

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
4. No se incluyen devengos considerando compensaciones (`reversal_of_*`) mediante importes efectivos (`effective_*`).
5. El sistema debe generar el fichero importable compatible con la AEAT.
6. No se gestionan compensaciones intertrimestrales en esta versión.
7. No se gestionan regímenes especiales de IVA (extensible).
8. Si un devengo tiene reverso total, su contribución fiscal neta es 0.
9. Los cálculos fiscales deben usar siempre importes efectivos (effective_*).


---

## Notas de diseño (no normativas)

> Nota: esta sección describe una posible aproximación. La arquitectura vinculante se define en los ADR.

## Arquitectura extensible

Para permitir nuevos informes fiscales:

- Definir una interfaz lógica común `FiscalReportGenerator`.
- Cada informe implementa:
  - validación de elegibilidad
  - selección de devengos
  - reglas de agregación
  - formato de salida
- El sistema debe permitir registrar nuevos generadores sin modificar los existentes.

---

## Capacidades

- Generar informe IRPF por propietario y año.
- Generar modelo 303 por trimestre.
- Exportar resultados en formato estructurado.
- Generar fichero compatible con AEAT para modelo 303.

---

## Fuera de alcance

- Presentación automática ante AEAT.
- Gestión de fraccionamientos o pagos.
- Gestión de otros modelos (111, 115, 390, etc.).
- Validación avanzada de coherencia tributaria.
- Ajustes por pagos reales (criterio de caja).

---

---

## Dependencias y trazabilidad

### Depende de
- (ninguna explícita)

### Impacto en contratos
- HTTP API: (si aplica)
- Eventos (CloudEvents): (si aplica)

---

## ADR aplicables

### Base
- ADR-0001
- ADR-0002
- ADR-0003
- ADR-0004
- ADR-0005
- ADR-0006
- ADR-0007
- ADR-0008
- ADR-0009
- ADR-0011
- ADR-0012

