# EN-0301: Application Service Modularization

## Objetivo
Reorganizar los servicios de la capa Application en módulos coherentes por dominio o bounded context para mejorar la mantenibilidad, reforzar los límites arquitectónicos y evitar acoplamiento excesivo entre casos de uso.

---

## Descripción
A medida que el sistema crece, la capa Application tiende a concentrar servicios y casos de uso en estructuras genéricas (por ejemplo “services” o “use_cases” globales). Esto incrementa el riesgo de:

- dependencias cruzadas no intencionales entre funcionalidades
- crecimiento descontrolado de módulos (“god modules”)
- duplicidad de conceptos y reglas
- dificultad para localizar y evolucionar casos de uso

Este enabler define una reorganización modular de la capa Application para agrupar casos de uso y servicios por dominios funcionales o bounded contexts, con fronteras explícitas. El objetivo es que cada módulo agrupe responsabilidades cohesionadas y minimice el acoplamiento con otros módulos.

La modularización debe preservar la arquitectura hexagonal: la capa Application continúa dependiendo únicamente de Domain (y de sus propios puertos), mientras que las implementaciones concretas permanecen en Infrastructure y se conectan en el composition root.

---

## Root afectado
- `backend/`

---

## Incluye
- Definición de una estructura modular en la capa Application basada en dominios funcionales o bounded contexts.
- Reorganización de:
  - casos de uso (application services)
  - puertos (ports) asociados
  - DTOs/modelos de entrada/salida de aplicación cuando existan
  - políticas/validaciones propias de aplicación (no de dominio)
- Reducción de dependencias cruzadas entre módulos de Application.
- Establecimiento de reglas explícitas para:
  - dependencias permitidas entre módulos (p.ej. prohibidas por defecto o mediante puertos)
  - ubicación de componentes “shared” (si existen) con criterios claros para evitar un “shared” monolítico.
- Mantenimiento de compatibilidad funcional: la reorganización no debe cambiar el comportamiento observable del sistema.

---

## Fuera de alcance
- Cambios en reglas de negocio del Domain.
- Cambios en contratos de adaptadores (HTTP/bot) o en la API pública.
- Cambios de persistencia, modelo ORM o estrategias de almacenamiento.
- Introducción de nuevos bounded contexts o redefinición funcional del dominio (solo reorganización estructural).

---

## Notas de arquitectura
- La modularización debe reforzar la dirección de dependencias: Application → Domain, nunca al revés.
- Las dependencias entre módulos de Application deben ser explícitas y mínimas, preferiblemente vía puertos o contratos definidos.
- Evitar la creación de un módulo “common/shared” sin criterios estrictos: solo se permite para componentes verdaderamente transversales y estables.
- El objetivo es mejorar la cohesión (módulos con responsabilidad clara) y reducir el acoplamiento (pocas dependencias entre módulos).

---

## Criterios de aceptación
1. La capa Application está organizada en módulos coherentes por dominio o bounded context, con fronteras claras.
2. No existen “god modules” en Application (módulos genéricos con responsabilidades dispares).
3. Las dependencias entre módulos de Application son mínimas y explícitas.
4. La reorganización no modifica el comportamiento funcional observable del sistema.
5. Se mantienen las reglas de arquitectura hexagonal y la inversión de dependencias definida en ADR-0002.