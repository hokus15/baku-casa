# Contexto del sistema — Baku.Casa

## Propósito del sistema

Baku.Casa es una aplicación self-hosted para la gestión de alquileres de inmuebles en España.

El sistema está pensado para propietarios particulares que desean automatizar la administración de sus propiedades y mantener un control claro sobre contratos, cobros y obligaciones fiscales asociadas al alquiler.

El objetivo del sistema es centralizar en una única herramienta la información y operaciones necesarias para la gestión de alquileres.

---

## Usuarios objetivo

El sistema está diseñado principalmente para:

- propietarios particulares de inmuebles
- usuarios que gestionan directamente sus propias propiedades

El sistema no está orientado a:

- uso multi-tenant
- plataformas SaaS
- gestión de propiedades para múltiples clientes

---

## Restricciones operativas

El sistema opera bajo las siguientes restricciones de contexto:

- despliegue **self-hosted**
- ejecución en **red local (LAN)**
- **infraestructura ligera** (por ejemplo Raspberry Pi o VPS pequeño)
- **sin dependencia obligatoria de servicios externos**
- **uso mono-usuario** en el alcance inicial

Estas restricciones forman parte del contexto del sistema y condicionan su diseño.

---

## Alcance funcional del sistema

Baku.Casa cubre progresivamente las siguientes áreas funcionales:

- gestión de propiedades
- gestión de titularidad de propiedades
- gestión de contratos de arrendamiento
- gestión económica de alquileres
- registro de devengos y pagos
- gestión de deudas y créditos
- generación de documentos asociados al alquiler
- soporte para reporting fiscal

El sistema no sustituye asesoramiento fiscal profesional.

---

## Automatización del sistema

El sistema puede generar eventos internos de forma automática para facilitar la gestión administrativa de los alquileres.

También permite integración con otros sistemas mediante mecanismos de automatización como:

- webhooks
- MQTT

---

## Enfoque del sistema

Baku.Casa está diseñado para ser:

- **determinista** en sus cálculos financieros
- **auditable**
- **reproducible**
- **controlado mediante especificaciones formales**

El desarrollo del sistema sigue un enfoque de **Specification Driven Development (SDD)**.

---

## Evolución del sistema

Las capacidades del sistema se introducen progresivamente mediante:

- **Features**, que introducen capacidades funcionales
- **Enablers**, que introducen capacidades técnicas o estructurales

La planificación del sistema se define en:

```
docs/roadmap.md
docs/dependency-graph.yaml
```

---

## Relación con otros documentos

Este documento describe únicamente el **contexto del sistema**.

Otros aspectos del sistema se definen en:

- `docs/constitution.md` — reglas invariantes del sistema
- `docs/roadmap.md` — planificación funcional
- `docs/dependency-graph.yaml` — dependencias entre Features y Enablers
- `docs/spec/` — especificaciones funcionales
- `docs/adr/` — decisiones arquitectónicas