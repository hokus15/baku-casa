# Roadmap Técnico — Evolución Incremental

---

# MVP 1 — Master Data y Contratos (Sin Registro Contable)

Objetivo:
Disponer de un sistema navegable y consistente que permita modelar toda la estructura contractual y reglas sin registrar todavía hechos económicos.

---

## F-0001 — Acceso y Autenticación
Acceso seguro mediante autenticación basada en tokens.

## F-0002 — Propietarios (Sujetos Fiscales)
Definición de propietarios como entidades fiscales independientes.

## F-0003 — Propiedades y Titularidad
Registro de inmuebles y vinculación a propietarios.

## F-0004 — Datos Económicos de la Propiedad
Registro de adquisición y datos patrimoniales.

## F-0005 — Gastos Recurrentes (Master Data)
Definición de plantillas de gastos periódicos.

## F-0006 — Contratos (Estructura Base)
Creación de contratos con condiciones básicas.

## F-0007 — Histórico de Rentas
Gestión del histórico de rentas por contrato.

## F-0008 — Cláusulas de Actualización de Renta
Definición de reglas de actualización (sin ejecución).

## F-0009 — Asignación de Gastos Recurrentes
Reasignación contractual de gastos al inquilino.

Resultado MVP1:
- Modelo de dominio completo.
- API madura y consistente.
- Sin registro de cargos ni pagos.
- Riesgo técnico bajo.

---

# MVP 2 — Núcleo Financiero (Ledger)

Objetivo:
Introducir el registro contable determinista como fuente única de verdad económica.

---

## F-0010 — Devengos
Registro de hechos económicos devengados (ingresos y gastos).

Entidad central del sistema financiero.

## F-0011 — Pagos, FIFO y Crédito
Registro de pagos y asignación automática FIFO sobre cargos abiertos.

Gestión de deudas y sobrepagos.

Resultado MVP2:
- Estado financiero real.
- Contratos con saldo.
- Base para facturación y reporting.
- Parte técnicamente más delicada del sistema.

---

# MVP 3 — Documentación Operativa

Objetivo:
Formalizar documentalmente la actividad económica ya existente.

---

## F-0012 — Facturación (Manual)
Emisión manual de facturas a partir de devengos facturables.

## F-0013 — Tareas (Manual)
Sistema de tareas supervisables ejecutadas manualmente.

Resultado MVP3:
- Sistema operativamente usable.
- Facturación formal.
- Base estructural para automatización.

---

# MVP 4 — Automatización Supervisada

Objetivo:
Reducir intervención manual generando tareas automáticamente.

---

## F-0014 — Automatización por Tareas
Generación automática de tareas basadas en:
- Rentas
- Gastos recurrentes
- Cláusulas
- Eventos temporales

Incluye uso de eventos (ADR-0010).

Resultado MVP4:
- Sistema semiautomático.
- Supervisión previa a ejecución.

---

# MVP 5 — Fiscalidad y Reporting

Objetivo:
Generar información consolidada para obligaciones fiscales.

---

## F-0015 — Reports Fiscales
Generación de resúmenes fiscales por propietario y periodo.

Resultado MVP5:
- Reporting estructurado.
- Base para modelos oficiales.