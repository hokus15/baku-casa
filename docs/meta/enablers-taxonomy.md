# Taxonomía de Enablers

Este documento define la taxonomía utilizada para clasificar **enablers técnicos** dentro del proyecto.

Los enablers representan trabajo técnico que **no introduce funcionalidad de dominio**, pero es necesario para soportar el desarrollo, la operación del sistema o la evolución de la arquitectura.

La taxonomía proporciona una estructura consistente para identificar, organizar y priorizar trabajo técnico.

---

## [purpose] Propósito

Esta taxonomía sirve para:

- clasificar enablers de forma consistente
- reducir ambigüedad al crear nuevos enablers
- facilitar la lectura del roadmap y del dependency graph
- ayudar a los LLM a inferir el tipo de capacidad técnica introducida por un enabler

---

## [category_en_01xx] EN-01xx — Infraestructura del Proyecto

Infraestructura necesaria para inicializar el repositorio y el entorno de desarrollo.

Estos enablers suelen aparecer en las primeras fases del proyecto.

Ejemplos:

- estructura del repositorio
- configuración de CI
- herramientas de desarrollo
- empaquetado básico

Ejemplos de enablers:

- **EN-0100 — Project Bootstrap**
- **EN-0101 — Deployment Packaging (Docker & Compose)**

---

## [category_en_02xx] EN-02xx — Infraestructura de Runtime

Capacidades necesarias para que el sistema funcione correctamente en ejecución.

Estos enablers cubren preocupaciones transversales del sistema.

Ejemplos:

- gestión de configuración
- logging estructurado
- publicación de eventos
- métricas y observabilidad
- idempotencia operativa
- protección contra duplicados

Ejemplos de enablers:

- **EN-0200 — Application Logging Baseline with Daily Rotation**
- **EN-0201 — In-Memory Database Testing Baseline**
- **EN-0202 — Configuration System**
- **EN-0208 — Domain Event Logging**
- **EN-0209 — Idempotency and Duplicate Operation Protection**

---

## [category_en_03xx] EN-03xx — Mejora de Arquitectura y Codebase

Refactorizaciones o mejoras estructurales que aumentan la calidad de la arquitectura sin modificar el comportamiento funcional del sistema.

Ejemplos:

- modularización
- refactor del composition root
- clarificación de límites entre capas
- reorganización interna de servicios
- consolidación del esquema de persistencia

Ejemplos de enablers:

- **EN-0300 — HTTP Composition Root Refactor**
- **EN-0301 — Application Service Modularization**
- **EN-0302 — Persistence Schema Rebaseline**

---

## [category_en_04xx] EN-04xx — Entrega y Operaciones

Capacidades relacionadas con el despliegue y operación del sistema.

Ejemplos:

- publicación de imágenes de contenedor
- automatización de migraciones
- automatización de despliegues

Ejemplos de enablers:

- **EN-0400 — Container Image Publishing**
- **EN-0401 — Database Migration Automation**

---

## [classification_criteria] Criterios de clasificación

Al clasificar un nuevo enabler, debe responderse primero a esta pregunta:

**¿Qué capacidad técnica introduce principalmente?**

Regla práctica:

- si introduce base de proyecto o tooling inicial → **EN-01xx**
- si introduce capacidad transversal de ejecución → **EN-02xx**
- si introduce mejora estructural o refactor arquitectónico → **EN-03xx**
- si introduce capacidad de entrega, despliegue u operación → **EN-04xx**

En caso de duda, debe elegirse la categoría que mejor describa el **resultado principal** del enabler, no un efecto secundario.

---

## [usage_guide] Guía de uso

Al crear un nuevo enabler:

1. Seleccionar la categoría adecuada.
2. Asignar el siguiente identificador disponible dentro de la categoría.
3. Describir **qué se quiere conseguir**, no **cómo se implementará**.
4. Referenciar ADR cuando el enabler dependa de decisiones arquitectónicas.

---

## [relationship_with_features_and_adrs] Relación con Features y ADR

| Artefacto | Propósito |
|---|---|
| Feature | Introduce funcionalidad de dominio |
| Enabler | Introduce capacidad técnica |
| ADR | Documenta decisiones arquitectónicas |

Los enablers pueden **referenciar ADR**, pero no deben redefinir decisiones arquitectónicas ya documentadas.

---

## [llm_notes] Notas para uso con LLMs

Esta taxonomía puede utilizarse como ayuda de clasificación, pero **no sustituye**:

- `docs/planning/dependency-graph.yaml` para dependencias y orden estructural
- `docs/planning/roadmap.md` para narrativa evolutiva
- `docs/specs/enablers/*` para la definición concreta de cada enabler
- `docs/decisions/adr/*` para decisiones arquitectónicas

La taxonomía debe utilizarse para responder a la pregunta:

**“Qué tipo de capacidad técnica representa este enabler?”**

No debe utilizarse como fuente de verdad de dependencias ni de orden de ejecución.