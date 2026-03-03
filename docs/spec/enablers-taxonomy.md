# Taxonomía de Enablers

## Propósito

Este documento define la taxonomía utilizada para clasificar **enablers técnicos** dentro del proyecto.

Los enablers representan trabajo técnico que **no introduce funcionalidad de dominio**, pero es necesario para soportar el desarrollo, la operación del sistema o la evolución de la arquitectura.

La taxonomía proporciona una estructura consistente para identificar, organizar y priorizar trabajo técnico.

---

# EN-01xx — Infraestructura del Proyecto

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

# EN-02xx — Infraestructura de Runtime

Capacidades necesarias para que el sistema funcione correctamente en ejecución.

Estos enablers cubren preocupaciones transversales del sistema.

Ejemplos:

- gestión de configuración
- logging estructurado
- publicación de eventos
- métricas y observabilidad

Ejemplos de enablers:

- **EN-0200 — Structured Logging**
- **EN-0201 — Configuration System**
- **EN-0202 — Event Publishing Infrastructure**

---

# EN-03xx — Mejora de Arquitectura y Codebase

Refactorizaciones o mejoras estructurales que aumentan la calidad de la arquitectura sin modificar el comportamiento funcional del sistema.

Ejemplos:

- modularización
- refactor del composition root
- clarificación de límites entre capas

Ejemplos de enablers:

- **EN-0300 — HTTP Composition Root Refactoring**
- **EN-0301 — Application Service Modularization**

---

# EN-04xx — Entrega y Operaciones

Capacidades relacionadas con el despliegue y operación del sistema.

Ejemplos:

- publicación de imágenes de contenedor
- automatización de migraciones
- automatización de despliegues

Ejemplos de enablers:

- **EN-0400 — Container Image Publishing**
- **EN-0401 — Database Migration Automation**

---

# Guía de uso

Al crear un nuevo enabler:

1. Seleccionar la categoría adecuada.
2. Asignar el siguiente identificador disponible dentro de la categoría.
3. Describir **qué se quiere conseguir**, no **cómo se implementará**.
4. Referenciar ADR cuando el enabler dependa de decisiones arquitectónicas.

---

# Relación con Features y ADR

| Artefacto | Propósito |
|---|---|
| Feature | Introduce funcionalidad de dominio |
| Enabler | Introduce capacidad técnica |
| ADR | Documenta decisiones arquitectónicas |

Los enablers pueden **referenciar ADR**, pero no deben redefinir decisiones arquitectónicas ya documentadas.