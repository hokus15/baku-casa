# EN-0300 — HTTP Application Bootstrap Modularization

## Objetivo

Reducir el acoplamiento en el punto de entrada de la aplicación HTTP del backend separando las responsabilidades de inicialización y garantizando que el composition root siga siendo el único lugar donde se conectan interfaces de Application con implementaciones de Infrastructure.

---

## Descripción

Actualmente el punto de entrada HTTP del backend concentra múltiples responsabilidades relacionadas con la inicialización de la aplicación, incluyendo la creación de la aplicación, el registro de dependencias, middleware, routers y manejadores de errores.

Esta acumulación de responsabilidades aumenta la complejidad del entrypoint y dificulta la mantenibilidad del composition root.

Este enabler introduce una separación clara de responsabilidades en el proceso de inicialización de la aplicación HTTP, de forma que cada aspecto del bootstrap pueda evolucionar de manera independiente sin aumentar el acoplamiento del punto de entrada.

El punto de entrada de la aplicación debe limitarse a iniciar la aplicación HTTP y delegar el proceso de bootstrap a componentes especializados.

La modularización del bootstrap permite que nuevos componentes de inicialización (por ejemplo middleware, routers o dependencias) puedan añadirse o modificarse sin alterar el punto de entrada de la aplicación.

---

## Root afectado

- `backend/`

---

## Incluye

- Separación de las responsabilidades del proceso de inicialización de la aplicación HTTP.
- Delegación del proceso de bootstrap desde el punto de entrada hacia componentes especializados.
- Organización del proceso de inicialización para mejorar la mantenibilidad del composition root.
- Garantía de que el registro de dependencias entre capas se realiza en un único punto central.

---

## Fuera de alcance

- Cambios en la lógica de negocio.
- Cambios en los contratos de la API HTTP.
- Introducción de nuevos middleware o routers.
- Modificaciones en el modelo de dominio o servicios de aplicación.

---

## Notas de arquitectura

El registro de dependencias debe seguir el principio de inversión de dependencias definido en **ADR-0002**, donde las interfaces de la capa Application se conectan con implementaciones de Infrastructure únicamente en el composition root.

La reorganización del proceso de inicialización no debe introducir dependencias que violen las reglas de arquitectura hexagonal.

---

## Criterios de aceptación

1. El punto de entrada HTTP deja de concentrar múltiples responsabilidades de inicialización.
2. El proceso de bootstrap de la aplicación se encuentra separado en componentes con responsabilidades claras.
3. El registro de dependencias entre capas sigue realizándose exclusivamente en el composition root.
4. La modularización del bootstrap mejora la claridad y mantenibilidad de la inicialización de la aplicación.
5. No se introducen dependencias que violen la arquitectura hexagonal definida en el proyecto.