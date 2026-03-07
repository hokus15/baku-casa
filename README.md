# Baku.Casa

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Architecture](https://img.shields.io/badge/architecture-hexagonal-blueviolet)
![Methodology](https://img.shields.io/badge/methodology-spec--driven-blue)
![Spec Kit](https://img.shields.io/badge/spec--kit-github-black)
![AI Generated Code](https://img.shields.io/badge/code-AI%20generated-orange)
![Human Code](https://img.shields.io/badge/human%20code-0%25-red)
![Deployment](https://img.shields.io/badge/deployment-self--hosted-lightgrey)
![Platform](https://img.shields.io/badge/platform-raspberry%20pi-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Aplicación **self-hosted** para la gestión de alquileres de inmuebles en España.

Pensada para propietarios particulares que quieren automatizar la administración de sus propiedades y tener control claro sobre contratos, cobros y obligaciones fiscales.

---

## Experimento de desarrollo

Este proyecto también sirve como **experimento práctico de desarrollo dirigido por especificaciones (Spec-Driven Development, SDD)**.

El objetivo es validar si es posible **crear una aplicación real y funcional desde cero guiando todo el desarrollo mediante especificaciones formales**, en lugar de comenzar directamente por la implementación.

Para ello se está utilizando **Spec-Kit**, el framework de GitHub para trabajar con SDD:

https://github.com/github/spec-kit

En este repositorio:

- Las funcionalidades se describen primero como **features**
- Las capacidades técnicas se modelan como **enablers**
- Cada unidad de trabajo tiene **spec, plan y tasks**
- El código se implementa únicamente después de que la especificación esté definida

Además, este experimento tiene un objetivo adicional:

> **No escribir ni modificar manualmente ninguna línea de código.**

Todo el desarrollo de la aplicación se delega en **agentes de IA** que implementan el sistema **exclusivamente a partir de las especificaciones**.

El rol humano en el proyecto se limita a:

- Definir **especificaciones funcionales**
- Tomar **decisiones arquitectónicas**
- Revisar los cambios propuestos por la IA

El código fuente final debe ser **resultado directo de las especificaciones**, no de programación manual.

Este enfoque permite explorar si un flujo basado en especificaciones:

- mejora la **reproducibilidad del desarrollo**
- reduce ambigüedades funcionales
- facilita el **trabajo con agentes de IA**
- permite reconstruir el sistema **a partir de la documentación**

---

# ¿Qué permite hacer?

## Gestión de propiedades y contratos

- Registro de propiedades
- Gestión de contratos de arrendamiento
- Control de fechas de inicio y fin
- Histórico de rentas

---

## Gestión económica

- Generación automática de devengos
- Aplicación de pagos con criterio FIFO
- Gestión de deudas y créditos
- Control de sobrepagos
- Modelado de gastos recurrentes

---

## Facturación y documentación

- Generación de recibos
- Emisión de facturas
- Representación clara de cargos y pagos aplicados

---

## Actualización de rentas

- Soporte para reglas de actualización (IPC, IRAV u otras)
- Aplicación controlada y auditable

---

## Soporte fiscal

- Preparación de información necesaria para:

  - IRPF
  - Modelo 303 (IVA)

El sistema **no sustituye asesoramiento fiscal profesional**.

---

## Automatización

- Generación automática de eventos internos
- Posibilidad de integración mediante **webhooks** o **MQTT**
- Automatización de tareas administrativas

---

# Características del sistema

- Funciona en **red local (LAN)**
- Despliegue **self-hosted**
- No depende de **servicios externos obligatorios**
- Diseñado para ejecutarse en **hardware ligero (por ejemplo Raspberry Pi)**
- Modelo de **usuario único** en el alcance inicial

---

# Enfoque

Baku está diseñado para ser:

- **Determinista** en sus cálculos financieros
- **Auditable**
- **Reproducible**
- **Controlado por especificaciones formales**

---

# Estado del proyecto

En desarrollo activo.

Las funcionalidades se implementan siguiendo un modelo de desarrollo basado en **especificaciones formales y decisiones arquitectónicas documentadas**.

---

## MVP 0 — Platform Bootstrap

| Item | Estado | Descripción |
|---|---|---|
| EN-0100 | ✅ Completado | Project Bootstrap |
| F-0001 | ✅ Completado | Acceso y Autenticación |
| EN-0202 | ✅ Completado | Configuration System — configuración centralizada y tipada |
| EN-0200 | ✅ Completado | Logging baseline con salida dual, correlación y rotación diaria |
| EN-0201 | ✅ Completado | Baseline de testing con DB en memoria para integración reproducible |
| EN-0300 | ✅ Completado | HTTP Bootstrap Modularization — thin entrypoint, composition root único, fail-fast |

---

## Observabilidad (EN-0200)

El backend aplica un baseline de logging estructurado con contrato operativo por entorno.

- Salida dual por evento: JSON + human-friendly.
- Campos mínimos obligatorios: `timestamp`, `level`, `service_name`, `correlation_id`, `message`.
- Timestamps de evento en UTC.
- Rotación diaria a las 00:00 Europe/Madrid.
- Retención inicial de 7 días para logs rotados (configurable por entorno).
- Fallback seguro si el perfil de logging falta o es inválido; no existe modo sin logging.