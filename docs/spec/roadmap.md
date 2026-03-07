# Roadmap Técnico — Evolución Incremental

Este roadmap define la evolución funcional del sistema y las capacidades técnicas necesarias para soportarlo.

Las funcionalidades del sistema se describen como **Features (F-xxxx)**.  
Las capacidades técnicas o estructurales se describen como **Enablers (EN-xxxx)**.

Los **Enablers** no introducen funcionalidad visible para el usuario final, pero habilitan el desarrollo seguro y mantenible de las features.

## Regla de baseline técnico acumulado

Las Features deben asumir como parte del sistema todos los Enablers previos que les apliquen según `docs/spec/dependency-graph.yaml`.

En particular, cualquier Enabler marcado con `affects_future_features: true` debe considerarse integrado en toda Feature futura aplicable, aunque no se repita explícitamente en su descripción funcional.

La aplicabilidad debe determinarse según:

- las dependencias directas e indirectas del dependency graph
- el alcance declarado del Enabler
- el contexto funcional y arquitectónico del roadmap

---

# MVP 0 — Platform Bootstrap

Objetivo:

Establecer la base técnica mínima del sistema y disponer de un primer flujo funcional para validar la arquitectura.

Incluye la inicialización del proyecto, configuración, observabilidad básica, testing y la primera feature funcional del sistema.

---

## EN-0100 — Project Bootstrap

**Estado: ✅ Completado**

Inicialización estructural del repositorio y configuración base del proyecto.

Incluye:

- estructura inicial del backend
- configuración de herramientas de desarrollo
- configuración básica del entorno de ejecución
- baseline del proyecto

---

## F-0001 — Acceso y Autenticación

**Estado: ✅ Completado**

Acceso seguro al sistema mediante autenticación basada en tokens.

Permite proteger los endpoints de la API y establecer la identidad del usuario.

---

## EN-0202 — Configuration System

**Estado: ✅ Completado**

Sistema centralizado y tipado para gestionar configuración de la aplicación.

Incluye:

- variables de entorno
- ficheros de configuración
- valores por defecto

Permite validar configuración en el arranque y garantizar consistencia entre entornos.

---

## EN-0200 — Application Logging Baseline with Daily Rotation

**Estado: ✅ Completado**

Sistema de logging estructurado con formato consistente.

Campos obligatorios:

- timestamp (UTC)
- level
- service_name
- correlation_id
- message

Los logs rotan diariamente a medianoche (Europe/Madrid).

Incluye:

- salida dual por evento (JSON + human-friendly)
- correlacion por request con `X-Correlation-ID`
- fallback seguro por entorno cuando el perfil de logging no es cargable

---

## EN-0201 — In-Memory Database Testing Baseline

Baseline de testing con base de datos en memoria para permitir:

- tests de integración rápidos
- ejecución reproducible en CI
- aislamiento entre tests

---

## EN-0300 — HTTP Composition Root Refactor

Reorganización del composition root HTTP para separar responsabilidades de bootstrap y mantener los límites de la arquitectura hexagonal.

---

Resultado MVP0:

- arquitectura base estable
- primer flujo funcional autenticado
- configuración centralizada
- observabilidad básica
- testing reproducible
- base técnica sólida para el desarrollo del dominio

---

# MVP 1 — Master Data y Contratos (Sin Registro Contable)

Las Features de MVP1 deben asumir como baseline todos los Enablers completados en MVP0 que les apliquen según `docs/spec/dependency-graph.yaml`, especialmente aquellos marcados como `affects_future_features: true`.

Objetivo:

Disponer de un sistema navegable que permita modelar completamente el dominio inmobiliario y la estructura contractual sin registrar todavía hechos económicos.

---

## F-0002 — Propietarios (Sujetos Fiscales)

Definición de propietarios como entidades fiscales independientes.

---

## F-0003 — Propiedades y Titularidad

Registro de inmuebles y vinculación a propietarios.

---

## F-0004 — Datos Económicos de la Propiedad

Registro de información económica asociada a la adquisición del inmueble.

---

## F-0005 — Gastos Recurrentes (Master Data)

Definición de plantillas de gastos periódicos asociados a propiedades.

---

## F-0006 — Contratos (Estructura Base)

Creación de contratos de alquiler con condiciones básicas.

---

## F-0007 — Histórico de Rentas

Gestión del histórico de rentas asociado a cada contrato.

---

## F-0008 — Cláusulas de Actualización de Renta

Definición de reglas de actualización de renta.

---

## F-0009 — Asignación de Gastos Recurrentes

Reasignación contractual de gastos al inquilino.

---

## EN-0301 — Application Service Modularization

Reorganización de los servicios de la capa Application en módulos coherentes por dominio o bounded context.

---

## EN-0207 — Pagination and List Query Conventions

Convenciones consistentes para endpoints que devuelven colecciones.

Incluye:

- parámetros de paginación
- ordenación
- estructura uniforme de respuesta

---

Resultado MVP1:

- modelo de dominio completo
- estructura contractual modelada
- API madura y consistente
- sistema navegable
- sin registro de cargos ni pagos

---

# MVP 2 — Núcleo Financiero (Ledger)

Las Features de MVP2 deben asumir como baseline todos los Enablers completados en MVP0 y MVP1 que les apliquen según `docs/spec/dependency-graph.yaml`, especialmente aquellos marcados como `affects_future_features: true`.

Objetivo:

Introducir el registro contable determinista como fuente única de verdad económica del sistema.

---

## F-0010 — Devengos

Registro de hechos económicos devengados (ingresos y gastos).

Constituye la entidad central del sistema financiero.

---

## EN-0209 — Idempotency and Duplicate Operation Protection

Protección contra ejecución duplicada de operaciones económicas críticas.

Permite reintentos seguros sin generar efectos económicos duplicados.

---

## F-0011 — Pagos, FIFO y Crédito

Registro de pagos realizados por los inquilinos.

Incluye:

- asignación automática FIFO
- gestión de deudas
- gestión de sobrepagos

---

## EN-0208 — Domain Event Logging

Registro de eventos relevantes del dominio en el sistema de logging estructurado.

Permite correlacionar eventos técnicos con eventos de negocio.

---

Resultado MVP2:

- estado financiero real del sistema
- contratos con saldo económico
- ledger consistente
- base para facturación y reporting

---

# MVP 3 — Documentación Operativa

Las Features de MVP3 deben asumir como baseline todos los Enablers completados en MVP0, MVP1 y MVP2 que les apliquen según `docs/spec/dependency-graph.yaml`, especialmente aquellos marcados como `affects_future_features: true`.

Objetivo:

Formalizar documentalmente las operaciones económicas registradas en el sistema.

---

## F-0012 — Facturación (Manual)

Emisión manual de facturas a partir de devengos facturables.

---

## F-0013 — Tareas (Manual)

Sistema de tareas supervisables ejecutadas manualmente.

---

Resultado MVP3:

- documentación económica formal
- sistema operativamente usable
- base para automatización futura

---

# MVP 4 — Automatización Supervisada

Las Features de MVP4 deben asumir como baseline todos los Enablers completados en MVP0, MVP1, MVP2 y MVP3 que les apliquen según `docs/spec/dependency-graph.yaml`, especialmente aquellos marcados como `affects_future_features: true`.

Objetivo:

Reducir intervención manual generando tareas automáticamente a partir de eventos del sistema.

---

## F-0014 — Automatización de Tareas

Generación automática de tareas basadas en:

- rentas
- gastos recurrentes
- cláusulas contractuales
- eventos temporales

Incluye uso de eventos definidos en ADR-0010.

---

Resultado MVP4:

- sistema parcialmente automatizado
- supervisión previa a ejecución
- reducción de trabajo manual

---

# MVP 5 — Fiscalidad y Reporting

Las Features de MVP5 deben asumir como baseline todos los Enablers completados en MVP0, MVP1, MVP2, MVP3 y MVP4 que les apliquen según `docs/spec/dependency-graph.yaml`, especialmente aquellos marcados como `affects_future_features: true`.

Objetivo:

Generar información consolidada para cumplimiento de obligaciones fiscales.

---

## F-0015 — Reports Fiscales

Generación de resúmenes fiscales por propietario y periodo.

---

Resultado MVP5:

- reporting estructurado
- base para generación de modelos fiscales
- explotación analítica de datos financieros