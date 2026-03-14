# Contexto del sistema — Baku.Casa

Este documento describe el **contexto operativo y el alcance del sistema**.

Contiene hechos y restricciones del entorno en el que opera Baku.Casa.

Este documento **NO define reglas del sistema**.  
Las reglas globales se definen exclusivamente en:

`docs/system/constitution.md`

---

# [system_purpose] 1. Propósito del sistema

Baku.Casa es una aplicación **self-hosted** para la gestión de alquileres de inmuebles.

Su objetivo es permitir a propietarios particulares:

- gestionar propiedades
- gestionar contratos de alquiler
- registrar eventos económicos
- controlar cobros y deudas
- generar información contable y fiscal

El sistema busca **automatizar la gestión de alquileres** manteniendo control total sobre los datos.

---

# [functional_scope] 2. Alcance funcional

El sistema cubre principalmente:

- gestión de propietarios (sujetos fiscales)
- gestión de propiedades
- gestión de contratos de alquiler
- registro de devengos (accruals)
- registro de pagos (payments)
- conciliación entre devengos y pagos
- generación de información económica

El sistema **NO pretende ser**:

- un ERP generalista
- un software contable completo
- un SaaS multi-usuario

---

# [user_model] 3. Modelo de usuario

El sistema está diseñado para un modelo **mono-operador**.

Características:

- un único operador administra el sistema
- no existe gestión compleja de permisos
- no existen roles múltiples de usuario

Los propietarios gestionados por el sistema **no son usuarios del sistema**.

Son entidades fiscales utilizadas para modelar la titularidad de propiedades.

---

# [geographic_scope] 4. Alcance geográfico y fiscal

El sistema está diseñado principalmente para el contexto de **España**.

Consecuencias:

- uso de moneda **EUR**
- gestión de propietarios con **NIF / CIF**
- adaptación al marco fiscal español para alquileres

El sistema **no está diseñado inicialmente para múltiples jurisdicciones fiscales**.

---

# [deployment_model] 5. Modelo de despliegue

Baku.Casa está diseñado para ejecutarse **self-hosted**.

Escenarios de despliegue previstos:

- ordenador personal
- servidor doméstico
- Raspberry Pi
- VPS ligero

El sistema se ejecuta normalmente mediante **contenedores Docker**.

---

# [infrastructure_constraints] 6. Restricciones de infraestructura

El sistema debe poder ejecutarse en entornos con recursos limitados.

Consecuencias:

- consumo de recursos moderado
- dependencia mínima de servicios externos
- instalación simple

El sistema **no debe requerir obligatoriamente servicios externos** para su funcionamiento básico.

---

# [access_model] 7. Modelo de acceso

El acceso al sistema se realiza normalmente a través de:

- API HTTP
- herramientas de desarrollo (ej. Postman)
- interfaces futuras (web o bots)

El sistema **no está pensado inicialmente para exposición pública en internet**.

---

# [persistence_context] 8. Persistencia

El sistema utiliza una base de datos relacional.

El almacenamiento está orientado a:

- simplicidad
- fiabilidad
- facilidad de despliegue

La tecnología concreta de persistencia se define mediante **ADR**.

---

# [operational_observability] 9. Observabilidad operativa

El sistema debe generar información suficiente para:

- diagnóstico de problemas
- auditoría operativa
- trazabilidad de operaciones

Los detalles técnicos de observabilidad se definen en la constitución y en los ADR.

---

# [system_evolution] 10. Evolución del sistema

El desarrollo del sistema sigue **Specification Driven Development (SDD)**.

Las capacidades del sistema evolucionan mediante:

- **Features** (capacidades funcionales)
- **Enablers** (capacidades técnicas)

El orden de implementación se define en:

`docs/planning/dependency-graph.yaml`

La planificación funcional se define en:

`docs/planning/roadmap.md`