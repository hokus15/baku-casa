# Constitución del sistema — Baku.Casa

Este documento define las reglas invariantes del sistema que gobiernan el diseño, planificación e implementación de Baku.Casa.

La constitución es la máxima autoridad normativa del sistema.

Este documento **DEBE permanecer agnóstico al stack concreto**.  
No debe fijar frameworks, librerías, herramientas o productos específicos salvo que formen parte de una restricción externa ineludible.

Las decisiones tecnológicas concretas **DEBEN documentarse mediante ADR**.

---

## [interpretation] Interpretación normativa

Las palabras **DEBE**, **NO DEBE**, **DEBERÍA** y **PUEDE** se interpretan según **RFC 2119**.

Estas palabras indican el nivel de obligatoriedad de cada regla.

---

# [constitution_scope] 1. Alcance de la constitución

Esta constitución define reglas invariantes del sistema.

Regula:

- arquitectura
- modelo económico
- representación de datos
- contratos externos
- operaciones
- observabilidad
- restricciones estructurales del sistema
- gobernanza del sistema

La constitución **NO define comportamiento funcional**.

El comportamiento funcional se define exclusivamente en:

- `docs/specs/features/*`
- `docs/specs/enablers/*`

La constitución **NO define decisiones tecnológicas concretas**.  
Esas decisiones se documentan en `docs/decisions/adr/*`.

---

# [sources_of_truth] 2. Fuentes de verdad del sistema

El sistema se define mediante los siguientes documentos:

- `docs/system/constitution.md`
- `docs/decisions/adr/*`
- `docs/planning/dependency-graph.yaml`
- `docs/specs/*`

En caso de conflicto:

**Constitution > ADR > Specification > Implementation**

Las especificaciones **NO DEBEN duplicar reglas definidas en esta constitución**.

---

# [single_source_of_truth] 3. Principio de fuente única de verdad

Cada regla del sistema **DEBE definirse en un único documento**.

Reglas globales del sistema **DEBEN definirse únicamente en esta constitución**.

Las especificaciones funcionales **NO DEBEN redefinir reglas ya definidas en la constitución**.  
Deben referenciarlas.

La duplicación de reglas en múltiples documentos **está prohibida**.

---

# [system_architecture] 4. Arquitectura del sistema

El backend **DEBE seguir arquitectura hexagonal**.

Capas permitidas:

- domain
- application
- interfaces
- infrastructure

Reglas:

- El dominio **NO DEBE depender de infraestructura**.
- La capa de aplicación **DEBE coordinar casos de uso**.
- La capa de interfaces **DEBE exponer adaptadores externos**.
- La infraestructura **DEBE implementar dependencias técnicas**.

---

# [model_separation] 5. Separación de modelos

El sistema **DEBE separar claramente**:

- modelos de dominio
- modelos de persistencia
- modelos de API o integración

Reglas:

- El dominio **NO DEBE depender de mecanismos concretos de persistencia**.
- Los contratos externos **NO DEBEN exponer modelos de persistencia**.
- Las conversiones entre capas **DEBEN ser explícitas**.

---

# [spec_vs_implementation] 6. Separación entre especificación e implementación

Las especificaciones describen **comportamiento esperado del sistema**.

Las especificaciones **NO DEBEN**:

- definir tecnologías
- definir frameworks
- definir estructura de código
- definir detalles de implementación

Las decisiones técnicas **DEBEN documentarse mediante ADR**.

---

# [economic_model] 7. Modelo económico del sistema

El sistema implementa un **modelo contable basado en ledger**.

Principios:

- El ledger es **append-only**.
- Los eventos económicos **NO SE MODIFICAN**.
- Las correcciones **se realizan mediante reversiones**.

Eventos económicos permitidos:

- Accrual
- Payment

Reglas:

- Los eventos **NO DEBEN eliminarse ni editarse**.
- Las reversiones **DEBEN crear nuevos eventos**.

---

# [accounting_invariants] 8. Invariantes contables

El sistema **DEBE preservar la conservación del valor económico**.

Reglas:

- Los importes **NO DEBEN ser negativos**.
- El signo económico **DEBE derivarse del tipo de evento**.
- Las compensaciones **DEBEN conservar el valor total**.
- Las compensaciones **DEBEN ser exactas**.

---

# [monetary_policy] 9. Política monetaria

Los importes monetarios **DEBEN representarse usando valores decimales exactos**.

Reglas:

- Los importes **DEBEN utilizar precisión decimal**.
- Está **prohibido utilizar floats para representar dinero**.
- Las operaciones monetarias **DEBEN preservar la precisión exacta**.

---

# [percentage_representation] 10. Porcentajes

Los porcentajes **DEBEN representarse en el rango 0–100 utilizando valores decimales**.

Reglas:

- El valor **0 representa el 0%**.
- El valor **100 representa el 100%**.
- Los porcentajes **DEBEN almacenarse usando precisión decimal**.
- Está **prohibido utilizar floats para representar porcentajes**.

---

# [time_policy] 11. Tiempo

Todas las fechas y horas **DEBEN almacenarse en UTC**.

Reglas:

- Las conversiones de zona horaria **DEBEN hacerse en la capa de presentación**.
- Las representaciones temporales expuestas externamente **DEBEN ser inequívocas**.

---

# [idempotency] 12. Idempotencia

Las operaciones que crean eventos económicos **DEBEN ser idempotentes**.

Reglas:

- El sistema **DEBE permitir identificar solicitudes repetidas**.
- Las solicitudes repetidas **NO DEBEN crear eventos duplicados**.

---

# [concurrency] 13. Concurrencia

Las operaciones económicas **DEBEN ser seguras ante concurrencia**.

Reglas:

- Las invariantes contables **NO DEBEN romperse bajo concurrencia**.
- Las operaciones críticas **DEBEN ejecutarse de forma transaccional**.

---

# [audit_fields] 14. Auditoría

Todas las entidades persistidas **DEBEN soportar auditoría**.

Campos obligatorios:

- created_at
- created_by
- updated_at
- updated_by
- deleted_at
- deleted_by

---

# [soft_delete] 15. Soft delete

Las entidades **NO DEBEN eliminarse físicamente**.

Reglas:

- El sistema **DEBE utilizar soft delete**.
- Los registros eliminados **NO DEBEN aparecer en consultas normales**.

---

# [api_contracts] 16. Contratos de API

El sistema **DEBE exponer contratos HTTP consistentes, versionables y orientados a recursos**.

Reglas:

- Los recursos **DEBEN representarse mediante contratos HTTP explícitos**.
- Las operaciones **DEBEN mapearse a semánticas HTTP estándar cuando aplique**.
- Los contratos externos **DEBEN ser validables y documentables**.

---

# [api_versioning] 17. Versionado de API

La versión mayor de la API **DEBE aparecer en la ruta base**.

Ejemplo:

```text
/api/v1
```

Reglas:

- Cambios incompatibles **DEBEN incrementar la versión mayor**.
- Cambios compatibles **DEBEN ser retrocompatibles**.

---

# [pagination] 18. Paginación

Los endpoints que devuelven colecciones **DEBEN estar paginados**.

Reglas:

- Está **prohibido devolver listas no acotadas**.
- El contrato de paginación **DEBE ser consistente**.

---

# [database_indexes] 19. Índices de base de datos

Los mecanismos de persistencia **DEBEN proporcionar estrategias de indexación adecuadas para consultas frecuentes y restricciones críticas**.

---

# [observability] 20. Observabilidad

El sistema **DEBE generar trazabilidad operativa suficiente para diagnóstico y auditoría**.

Reglas:

- Los eventos operativos relevantes **DEBEN quedar registrados de forma estructurada**.
- Las operaciones correlacionables **DEBEN incluir identificadores de correlación**.
- Los fallos **NO DEBEN perderse de forma silenciosa**.

---

# [infrastructure] 21. Infraestructura

El sistema **DEBE poder ejecutarse en entornos domésticos o VPS ligeros**.

Reglas:

- El sistema **NO DEBE depender obligatoriamente de servicios externos** para su funcionamiento básico.
- El despliegue **DEBE seguir siendo viable con recursos limitados**.

---

# [technical_baseline] 22. Baseline técnico del sistema

Los **Enablers introducen capacidades técnicas reutilizables**.

Los Enablers marcados como `affects_future_features: true` en el dependency graph forman parte del **baseline técnico del sistema**.

Las Features futuras **DEBEN asumir la existencia de ese baseline** y **NO deben redefinir esas capacidades**.

---

# [principle_of_least_surprise] 23. Principio de mínima sorpresa

Las especificaciones deben:

- ser deterministas
- evitar ambigüedad
- evitar comportamiento implícito

Si una regla puede interpretarse de múltiples formas, la especificación **DEBE aclararla explícitamente**.

---

# [engineering_principles] 24. Principios de ingeniería

El desarrollo **DEBE seguir Specification Driven Development (SDD)**.

Reglas:

- Las capacidades **se introducen mediante Features y Enablers**.
- Las implementaciones **DEBEN seguir las especificaciones**.

---

# [system_governance] 25. Gobernanza del sistema

Las modificaciones que rompan reglas de esta constitución **DEBEN actualizar la constitución**.

Las modificaciones incompatibles **DEBEN documentarse mediante ADR**.
