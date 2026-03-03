# EN-0300: HTTP Composition Root Refactoring

## Objetivo

Mejorar la claridad y mantenibilidad del punto de entrada HTTP del backend separando las responsabilidades de inicialización de la aplicación en módulos dedicados.

Este enabler asegura que el composition root permanezca simple y explícito, evitando que el módulo principal acumule lógica de configuración.

---

## Descripción

Actualmente el punto de entrada del backend concentra múltiples responsabilidades relacionadas con la inicialización de la aplicación HTTP.

Este enabler introduce una estructura modular para la configuración de la aplicación, separando:

- creación de la aplicación HTTP
- registro de dependencias
- registro de middleware
- registro de routers
- registro de manejadores de errores

El objetivo es mantener el composition root claro y facilitar la evolución del sistema conforme crezca el número de dependencias y adaptadores.

---

## Alcance

Este enabler incluye:

- reorganización del código de inicialización del backend HTTP
- extracción de la configuración de dependencias a un módulo dedicado
- separación del registro de middleware, routers y error handlers
- simplificación del punto de entrada de la aplicación

---

## Fuera de alcance

Este enabler no incluye:

- cambios en la lógica de dominio
- cambios en casos de uso de aplicación
- cambios en contratos HTTP existentes
- cambios en comportamiento funcional del sistema

---

## Criterios de aceptación

- El módulo principal de arranque del backend queda limitado a la creación de la aplicación.
- La configuración de dependencias se encuentra en un módulo separado.
- Middleware, routers y error handlers se registran mediante funciones de configuración dedicadas.
- No se modifica el comportamiento observable de la API.

---

## Notas de arquitectura

Este enabler debe respetar:

- la arquitectura hexagonal definida en la constitución
- la separación estricta entre Interfaces e Infrastructure
- el principio de composition root como único lugar donde se conectan implementaciones concretas

No debe introducir nuevos frameworks de inyección de dependencias.