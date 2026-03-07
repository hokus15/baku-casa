# F-0012: Facturación

## Objetivo

Emitir facturas a partir de devengos (`Accrual`) **facturables**, utilizando exclusivamente la información fiscal almacenada en los propios devengos.

La factura es una **representación documental y fiscal** de uno o varios devengos.  
No constituye un nuevo hecho económico ni altera el saldo contable del sistema.

Regla base: si un devengo tiene IVA (`vat_rate_percent > 0`), entonces **siempre es facturable**.

---

## Definiciones

- **Factura**: documento fiscal emitido a un cliente (inquilino) que agrupa uno o varios devengos facturables.
- **Devengo facturable**: devengo con `vat_rate_percent > 0`.
- **Línea de factura**: referencia a un devengo incluida en una factura.
- **Cardinalidad por defecto**: una factura agrupa 1 único `Accrual` (normalmente la renta mensual).
- **Excepciones permitidas** (explícitas): una factura PUEDE agrupar múltiples `Accrual` facturables cuando:
  - pertenecen al mismo `contract_id`, y
  - tienen el mismo destinatario fiscal (tenant) y mismo emisor fiscal (owner/supplier_snapshot), y
  - son compatibles en serie/criterio de numeración (si aplica).
- **Emisión**: transición de un borrador a una factura emitida (inmutable).
- **Factura rectificativa**: factura emitida que compensa total o parcialmente otra factura emitida.
- **Serie**: identificador lógico para numeración de facturas (si aplica).

---

## Entidades

### Invoice

**Campos obligatorios**

- `invoice_id`
- `issue_date`: date
- `status`: enum { `DRAFT`, `ISSUED` }
- `customer_snapshot`: object (datos fiscales del destinatario en el momento de emisión)
- `supplier_snapshot`: object (datos fiscales del emisor en el momento de emisión)

**Campos opcionales**

- `series`: string
- `number`: string (o integer) — asignado al emitir
- `notes`: string
- `reversal_of_invoice_id`: opaque id (opcional)

**Campos derivados (no persistidos)**

- `base_total`
- `vat_total`
- `withholding_total`
- `gross_total`
- `net_payable_total`
- `effect_sign`:
  - `+1` si `reversal_of_invoice_id` es null
  - `-1` si `reversal_of_invoice_id` existe
- `effective_base_total = effect_sign * base_total`
- `effective_vat_total = effect_sign * vat_total`
- `effective_withholding_total = effect_sign * withholding_total`
- `effective_gross_total = effect_sign * gross_total`
- `effective_net_payable_total = effect_sign * net_payable_total`

---

### InvoiceLine

**Campos obligatorios**

- `invoice_id`
- `accrual_id`
- `description`
- `base_amount` (decimal positivo o cero)
- `vat_rate_percent` (0–100)
- `withholding_rate_percent` (0–100)

**Campos derivados (no persistidos)**

- `vat_amount = base_amount * vat_rate_percent / 100`
- `withholding_amount = base_amount * withholding_rate_percent / 100`
- `gross_amount = base_amount + vat_amount`
- `net_payable_amount = gross_amount - withholding_amount`

Todos los importes persistidos son siempre positivos o cero.

---

## Capacidades

- Crear factura en borrador a partir de devengos facturables.
- Listar facturas (por rango de fechas, estado).
- Consultar detalle de factura con sus líneas.
- Emitir factura (asignar numeración/serie y congelar snapshots).
- Generar factura rectificativa que compense total o parcialmente una factura emitida.

---

## Alcance

- Facturación basada exclusivamente en `Accrual`.
- Una línea de factura corresponde a un devengo facturable.
- Totales calculados a partir de los porcentajes del devengo.
- Soporte de retención (`withholding_rate_percent`) cuando aplique.
- Soporte de rectificación mediante compensación.
- Importes siempre persistidos como valores positivos.

---

## Fuera de alcance

- Numeración legal avanzada multi-serie con reglas complejas.
- Motivos legales obligatorios de rectificación.
- Plantillas PDF/HTML finales y firma digital.
- Integración con SII/VeriFactu u otros sistemas tributarios.
- Cobro automático.
- Recalculo automático de devengos al rectificar facturas.

---

## Reglas de negocio

1. Solo pueden facturarse devengos con `vat_rate_percent > 0`.
2. Un devengo facturable debe ser:
   - `type = INCOME`
   - `payer = TENANT`
   - `contract_id` obligatorio.
3. La factura se construye exclusivamente desde devengos (fuente única).
4. Una factura en estado `DRAFT` puede eliminarse.
5. Una factura en estado `ISSUED` es inmutable.
6. Una factura emitida no puede cancelarse ni modificarse.
7. Para corregir una factura emitida debe crearse una nueva factura con:
   - `reversal_of_invoice_id` apuntando a la factura original.
8. Los importes de una factura rectificativa deben ser positivos.
9. El efecto económico de una factura rectificativa es negativo y se deriva mediante `effect_sign`.
10. No puede revertirse más importe del originalmente facturado.
11. No puede crearse una rectificativa sobre una factura ya completamente revertida.
12. La factura rectificativa debe tener el mismo `customer_snapshot` que la original.
13. Los importes de cada línea se derivan del devengo asociado.
14. Los totales de factura se derivan como sumatorio de líneas.
15. Las facturas no alteran el saldo contable ni la deuda del contrato; el saldo se calcula exclusivamente desde `Accrual` y `Payment`.
16. La emisión de factura no modifica el devengo subyacente.
17. Si el error está en el devengo, debe corregirse primero mediante un `Accrual` compensatorio antes de emitir la rectificativa correspondiente.
18. Si un `Accrual` facturado se corrige mediante un `Accrual` compensatorio, la rectificativa DEBE incluir como línea el `Accrual` compensatorio (o los compensatorios) correspondiente(s).
19. Un `accrual_id` solo puede aparecer en líneas de facturas emitidas cuya suma efectiva no exceda el importe efectivo del devengo.
20. Si un devengo ya ha sido completamente facturado (considerando rectificativas), no puede volver a incluirse en una nueva factura.
21. Regla por defecto: la factura se emite para un único `Accrual` (renta).
22. Se permite agrupar múltiples `Accrual` facturables en una misma factura SOLO si:
   - todos pertenecen al mismo `contract_id`,
   - comparten `payer = TENANT` y el mismo destinatario fiscal,
   - y los snapshots (`customer_snapshot`, `supplier_snapshot`) son consistentes para todas las líneas.
23. Una `InvoiceLine` siempre referencia exactamente un `accrual_id`.

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


---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Correlacion por request mediante `correlation_id`.
