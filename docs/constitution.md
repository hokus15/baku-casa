# Constitución del sistema — Baku.Casa

## Interpretación normativa

Las palabras DEBE, NO DEBE, DEBERÍA y PUEDE se interpretan según RFC 2119.

Estas palabras indican el nivel de obligatoriedad de cada regla.

---

# 1. Alcance de la constitución

Esta constitución define reglas invariantes del sistema.

Regula:

- arquitectura
- modelo económico
- representación de datos
- contratos de API
- persistencia
- operaciones
- observabilidad
- gobernanza del sistema

La constitución no define comportamiento funcional.

El comportamiento funcional se define exclusivamente en:

docs/spec/features/*
docs/spec/enablers/*

---

# 2. Fuentes de verdad del sistema

El sistema se define mediante los siguientes documentos:

- docs/constitution.md
- docs/adr/*
- docs/dependency-graph.yaml
- docs/spec/*

En caso de conflicto:

Constitution > ADR > Specification > Implementation

Las especificaciones NO DEBEN duplicar reglas definidas en esta constitución.

---

# 3. Principio de fuente única de verdad

Cada regla del sistema DEBE definirse en un único documento.

Reglas globales del sistema DEBEN definirse únicamente en esta constitución.

Las especificaciones funcionales NO DEBEN redefinir reglas ya definidas en la constitución.
Deben referenciarlas.

La duplicación de reglas en múltiples documentos está prohibida.

---

# 4. Arquitectura del sistema

El backend DEBE seguir arquitectura hexagonal.

Capas permitidas:

domain  
application  
interfaces  
infrastructure  

Reglas:

- El dominio NO DEBE depender de infraestructura.
- La capa de aplicación coordina casos de uso.
- Interfaces expone adaptadores externos.
- Infraestructura implementa dependencias técnicas.

---

# 5. Separación de modelos

El sistema DEBE separar claramente:

- modelos de dominio
- modelos de persistencia (ORM)
- modelos de API

Reglas:

- El dominio NO DEBE depender de ORM.
- Los DTOs de API NO DEBEN exponer entidades ORM.
- Las conversiones entre capas DEBEN ser explícitas.

---

# 6. Separación entre especificación e implementación

Las especificaciones describen comportamiento esperado del sistema.

Las especificaciones NO DEBEN:

- definir tecnologías
- definir frameworks
- definir estructura de código
- definir detalles de implementación

Las decisiones técnicas deben documentarse mediante ADR.

---

# 7. Modelo económico del sistema

El sistema implementa un modelo contable basado en ledger.

Principios:

- El ledger es append-only.
- Los eventos económicos NO SE MODIFICAN.
- Las correcciones se realizan mediante reversiones.

Eventos económicos permitidos:

Accrual  
Payment  

Reglas:

- Los eventos NO DEBEN eliminarse ni editarse.
- Las reversiones DEBEN crear nuevos eventos.

---

# 8. Invariantes contables

El sistema DEBE preservar la conservación del valor económico.

Reglas:

- Los importes NO DEBEN ser negativos.
- El signo económico DEBE derivarse del tipo de evento.
- Las compensaciones DEBEN conservar el valor total.
- Las compensaciones DEBEN ser exactas.

---

# 9. Política monetaria

Los importes monetarios DEBEN representarse usando valores decimales exactos.

Reglas:

- Los importes DEBEN utilizar precisión decimal.
- Está prohibido utilizar floats para representar dinero.
- Las operaciones monetarias DEBEN preservar la precisión exacta.

---

# 10. Porcentajes

Los porcentajes DEBEN representarse en el rango 0–100 utilizando valores decimales.

Reglas:

- El valor 0 representa el 0%.
- El valor 100 representa el 100%.
- Los porcentajes DEBEN almacenarse usando precisión decimal.
- Está prohibido utilizar floats para representar porcentajes.

---

# 11. Tiempo

Todas las fechas y horas DEBEN almacenarse en UTC.

Reglas:

Las conversiones de zona horaria DEBEN hacerse en la capa de presentación.

---

# 12. Idempotencia

Las operaciones que crean eventos económicos DEBEN ser idempotentes.

Reglas:

- El sistema DEBE permitir identificar solicitudes repetidas.
- Las solicitudes repetidas NO DEBEN crear eventos duplicados.

---

# 13. Concurrencia

Las operaciones económicas DEBEN ser seguras ante concurrencia.

Reglas:

- Las invariantes contables NO DEBEN romperse bajo concurrencia.
- Las operaciones críticas DEBEN ejecutarse de forma transaccional.

---

# 14. Auditoría

Todas las entidades persistidas DEBEN soportar auditoría.

Campos obligatorios:

created_at  
created_by  
updated_at  
updated_by  
deleted_at  
deleted_by  

---

# 15. Soft delete

Las entidades NO DEBEN eliminarse físicamente.

Reglas:

- El sistema DEBE utilizar soft delete.
- Los registros eliminados NO DEBEN aparecer en consultas normales.

---

# 16. Contratos de API

La API DEBE ser RESTful.

Reglas:

- Los recursos DEBEN representarse como recursos HTTP.
- Las operaciones DEBEN mapearse a métodos HTTP estándar.

---

# 17. Versionado de API

La versión mayor de la API DEBE aparecer en la ruta base.

Ejemplo:

/api/v1

Reglas:

- Cambios incompatibles DEBEN incrementar la versión mayor.
- Cambios compatibles DEBEN ser retrocompatibles.

---

# 18. Paginación

Los endpoints que devuelven colecciones DEBEN estar paginados.

Reglas:

- Está prohibido devolver listas no acotadas.
- El contrato de paginación DEBE ser consistente.

---

# 19. Índices de base de datos

Las tablas DEBEN tener índices adecuados para consultas frecuentes.

---

# 20. Observabilidad

El sistema DEBE generar logs estructurados.

Reglas:

- Los logs DEBEN estar en inglés.
- Los logs DEBEN incluir correlation id.

---

# 21. Infraestructura

El sistema DEBE poder ejecutarse en entornos domésticos o VPS ligeros.

Reglas:

- El sistema NO DEBE depender obligatoriamente de servicios externos.

---

# 22. Baseline técnico del sistema

Los Enablers introducen capacidades técnicas reutilizables.

Los Enablers marcados como `affects_future_features: true` en el dependency graph
forman parte del baseline técnico del sistema.

Las Features futuras DEBEN asumir la existencia de ese baseline
y no deben redefinir esas capacidades.

---

# 23. Principio de mínima sorpresa

Las especificaciones deben:

- ser deterministas
- evitar ambigüedad
- evitar comportamiento implícito

Si una regla puede interpretarse de múltiples formas,
la especificación debe aclararla explícitamente.

---

# 24. Principios de ingeniería

El desarrollo DEBE seguir Specification Driven Development (SDD).

Reglas:

- Las capacidades se introducen mediante Features y Enablers.
- Las implementaciones DEBEN seguir las especificaciones.

---

# 25. Gobernanza del sistema

Las modificaciones que rompan reglas de esta constitución DEBEN actualizar la constitución.

Las modificaciones incompatibles DEBEN documentarse mediante ADR.