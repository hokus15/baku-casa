# Feature Specification: F-0003 - Propiedades y Titularidad

**Feature Branch**: `001-propiedades-titularidad`  
**Created**: 2026-03-09  
**Status**: Draft  
**Roadmap Item**: F-0003  
**Phase**: MVP1

## Context and Scope

F-0003 incorpora el registro de propiedades y la titularidad actual de cada propiedad respecto a uno o varios propietarios ya existentes.

Este alcance crea la base de master data necesaria para features posteriores de contratos, datos economicos, contabilidad y reporting fiscal, sin introducir aun operaciones economicas del ledger.

---

## Clarifications

### Session 2026-03-10

- Q: Cual es el total permitido para la suma de `ownership_percentage`? -> A: El total permitido es 100; se acepta suma menor y se rechaza suma mayor.
- Q: Que precision decimal se permite para `ownership_percentage`? -> A: Hasta 2 decimales.
- Q: Cuales son los parametros de paginacion para listados? -> A: `page=1`, `page_size=20`, `max_page_size=100`, con `page_size` y `max_page_size` configurables transversalmente para todas las listas.
- Q: Se permite mas de una titularidad activa por el mismo par propiedad-propietario? -> A: No; solo una titularidad activa por (`property_id`, `owner_id`).
- Q: Cual es el formato temporal y de fechas para esta feature? -> A: `timestamps` en ISO-8601 UTC con sufijo `Z`; fechas puras en `YYYY-MM-DD`.

---

## Baseline Enablers Applied

Los siguientes Enablers completados y marcados como `affects_future_features: true` forman parte del baseline aplicable a F-0003 segun `docs/dependency-graph.yaml`:

| Enabler | Estado | Impacto en F-0003 |
|---------|--------|-------------------|
| EN-0100 | done | Base estructural de proyecto y disciplina de roots |
| EN-0202 | done | Configuracion centralizada y validacion fail-fast |
| EN-0200 | done | Logging estructurado y correlacion por request |
| EN-0201 | done | Baseline de pruebas de integracion con DB en memoria |
| EN-0300 | done | Composition root HTTP modular y limites arquitectonicos |

Dependencias funcionales previas relevantes:

- F-0001 (done): autenticacion de operador ya disponible para proteger operaciones.
- F-0002 (done): propietarios/sujetos fiscales disponibles para asignar titularidad.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar propiedad con titularidad inicial (Priority: P1)

Como operador autenticado, quiero dar de alta una propiedad y asignarle su titularidad actual para que la propiedad quede disponible como referencia valida para procesos posteriores del dominio.

**Why this priority**: Sin alta de propiedad con titularidad valida no existe base util para contratos ni datos economicos posteriores.

**Independent Test**: Se valida creando una propiedad con datos obligatorios y una o varias titularidades, comprobando que la propiedad queda activa y consultable con sus propietarios asociados.

**Acceptance Scenarios**:

1. **Given** un operador autenticado y propietarios existentes, **When** registra una propiedad con `name`, `type` valido y titularidad inicial valida, **Then** el sistema crea la propiedad, registra auditoria (`created_at`, `created_by`, `updated_at`, `updated_by`) y devuelve el detalle con titulares activos.
2. **Given** un operador autenticado, **When** intenta crear una propiedad con un `type` fuera de la lista cerrada, **Then** el sistema rechaza la solicitud con error tipificado de validacion y no crea la propiedad.
3. **Given** un operador autenticado, **When** intenta crear una propiedad sin titulares, **Then** el sistema rechaza la solicitud por incumplir la regla de minimo un propietario.
4. **Given** un operador no autenticado, **When** intenta crear una propiedad, **Then** el sistema responde no autenticado.

---

### User Story 2 - Consultar propiedades y relaciones de titularidad (Priority: P2)

Como operador autenticado, quiero consultar propiedades y sus titulares para revisar la situacion actual de titularidad desde ambos lados (propiedad y propietario).

**Why this priority**: La consulta de estado actual es necesaria para operar el sistema y preparar decisiones en features dependientes.

**Independent Test**: Se valida listando propiedades activas, consultando detalle de una propiedad, listando propiedades por propietario y propietarios por propiedad.

**Acceptance Scenarios**:

1. **Given** propiedades activas registradas, **When** el operador lista propiedades, **Then** obtiene una coleccion paginada de propiedades activas sin incluir eliminadas logicamente.
2. **Given** una propiedad activa con varios titulares, **When** el operador consulta su detalle, **Then** obtiene la titularidad activa completa con porcentajes.
3. **Given** un propietario con varias propiedades activas, **When** el operador consulta sus propiedades, **Then** obtiene solo relaciones de titularidad activas.
4. **Given** una propiedad eliminada logicamente, **When** el operador ejecuta consultas normales, **Then** la propiedad y sus titularidades asociadas no aparecen en resultados activos.

---

### User Story 3 - Actualizar propiedad y titularidad actual (Priority: P3)

Como operador autenticado, quiero editar datos de la propiedad y ajustar porcentajes de titularidad para mantener la informacion actualizada sin historico.

**Why this priority**: La informacion maestra pierde valor si no puede mantenerse actualizada ante cambios.

**Independent Test**: Se valida editando campos permitidos de la propiedad y modificando porcentajes de titulares existentes, comprobando actualizacion de `updated_at` y `updated_by`.

**Acceptance Scenarios**:

1. **Given** una propiedad activa, **When** el operador actualiza campos editables, **Then** el sistema persiste cambios y actualiza metadatos de auditoria de modificacion.
2. **Given** una propiedad activa con varios titulares, **When** el operador modifica los porcentajes, **Then** el sistema valida que cada porcentaje este en rango 0-100 y acepta la operacion aunque la suma total quede por debajo de 100.
3. **Given** una propiedad activa, **When** el operador intenta editar campos derivados (`cadastral_construction_value`, `construction_ratio`), **Then** el sistema rechaza la edicion directa.

---

### User Story 4 - Eliminar propiedad con soft-delete (Priority: P4)

Como operador autenticado, quiero eliminar una propiedad sin borrado fisico para mantener trazabilidad y consistencia historica en entidades de master data.

**Why this priority**: La baja logica protege la integridad historica y evita perdida irreversible de referencias de dominio.

**Independent Test**: Se valida eliminando logicamente una propiedad y comprobando que deja de verse como activa y que sus relaciones de titularidad reciben soft-delete en cascada sin borrado fisico.

**Acceptance Scenarios**:

1. **Given** una propiedad activa, **When** el operador solicita eliminacion, **Then** el sistema registra `deleted_at` y `deleted_by` y excluye la propiedad de consultas activas.
2. **Given** una propiedad eliminada logicamente, **When** se consultan titularidades activas, **Then** las relaciones asociadas no se incluyen porque fueron marcadas con soft-delete en cascada.
3. **Given** un identificador inexistente, **When** el operador solicita eliminacion, **Then** el sistema devuelve error tipificado de no encontrado.

---

### Edge Cases

- Que ocurre cuando la suma de porcentajes de titularidad no alcanza exactamente 100: la operacion se acepta y la propiedad mantiene titularidad parcial segun la regla funcional vigente.
- Que ocurre cuando la suma de porcentajes de titularidad supera 100: la operacion se rechaza por validacion.
- Que ocurre cuando algun `ownership_percentage` esta fuera del rango 0-100: la operacion se rechaza.
- Que ocurre cuando algun `ownership_percentage` tiene mas de 2 decimales: la operacion se rechaza por validacion.
- Que ocurre cuando se informa `cadastral_value` igual a 0 y existe valor de construccion o suelo: el sistema evita division invalida y trata `construction_ratio` como no aplicable.
- Que ocurre cuando se elimina una propiedad con titularidades activas: las titularidades permanecen almacenadas pero pasan a estado inactivo para consultas normales.
- Que ocurre cuando se intenta asociar un propietario inexistente a una propiedad: el sistema rechaza la operacion por referencia invalida.
- Que ocurre cuando se intenta crear una segunda titularidad activa para el mismo par (`property_id`, `owner_id`): la operacion se rechaza por duplicidad.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE permitir crear propiedades con `property_id` opaco e inmutable, `name` y `type` obligatorio, y titularidad inicial valida.
- **FR-002**: El sistema DEBE validar `type` contra el conjunto cerrado definido: Vivienda, Apartamento, Plaza de aparcamiento, Estudio, Local comercial, Oficina, Trastero, Otro.
- **FR-003**: El sistema DEBE permitir registrar y mantener como opcionales los campos descriptivos, de localizacion, catastrales y fiscales definidos en el roadmap item.
- **FR-004**: El sistema DEBE calcular `cadastral_construction_value` como diferencia entre valor catastral total y valor catastral de suelo cuando ambos valores esten informados.
- **FR-005**: El sistema DEBE calcular `construction_ratio` como porcentaje derivado de `cadastral_construction_value` sobre `cadastral_value` cuando el calculo sea aplicable.
- **FR-006**: El sistema DEBE impedir la edicion directa de campos derivados (`cadastral_construction_value`, `construction_ratio`).
- **FR-007**: El sistema DEBE permitir asociar una propiedad a uno o varios propietarios existentes mediante relaciones de titularidad con `ownership_percentage`.
- **FR-007a**: El sistema DEBE garantizar como invariante que exista como maximo una titularidad activa por cada par (`property_id`, `owner_id`).
- **FR-008**: El sistema DEBE exigir que toda propiedad activa tenga al menos un titular activo.
- **FR-009**: El sistema DEBE validar que cada `ownership_percentage` este en rango 0-100 con precision maxima de 2 decimales.
- **FR-010**: El sistema DEBE aceptar operaciones de alta o modificacion de titularidad aunque la suma de `ownership_percentage` no alcance 100.
- **FR-011**: El sistema DEBE rechazar operaciones de titularidad cuando la suma de `ownership_percentage` supere 100.
- **FR-012**: El sistema DEBE permitir modificar porcentajes de titularidad de una propiedad activa manteniendo las invariantes de validacion.
- **FR-013**: El sistema DEBE permitir consultar detalle de propiedad, listar propiedades, consultar propiedades por propietario y propietarios por propiedad, siempre sobre estado actual activo por defecto.
- **FR-014**: El sistema DEBE aplicar paginacion consistente en consultas de coleccion de propiedades usando `page` (default 1) y `page_size` (default 20, maximo 100).
- **FR-014a**: `page_size` y `max_page_size` DEBEN ser configurables de forma transversal para todos los endpoints de coleccion de la API, manteniendo consistencia con el baseline de paginacion.
- **FR-015**: El sistema DEBE aplicar soft-delete en propiedades mediante `deleted_at` y `deleted_by`, sin borrado fisico.
- **FR-016**: Cuando una propiedad se elimina logicamente, el sistema DEBE aplicar soft-delete en cascada sobre sus titularidades asociadas, registrando `deleted_at` y `deleted_by` tambien en dichas relaciones.
- **FR-017**: El sistema DEBE registrar auditoria estructural en entidades modificables de esta feature: `created_at`, `created_by`, `updated_at`, `updated_by`, y en borrado logico `deleted_at`, `deleted_by`.
- **FR-018**: Todos los `timestamps` de auditoria DEBEN gestionarse en UTC y serializarse en formato ISO-8601 con sufijo `Z`.
- **FR-018a**: Los campos de fecha sin componente temporal (por ejemplo, `acquisition_date`, `transfer_date`) DEBEN representarse como `YYYY-MM-DD`.
- **FR-019**: Todas las operaciones de esta feature DEBEN requerir operador autenticado segun la capacidad ya establecida en F-0001.
- **FR-020**: Los errores funcionales DEBEN devolverse como errores tipificados con codigo estable en ingles, mensaje descriptivo en espanol y `correlation_id`.
- **FR-021**: Los registros de observabilidad de esta feature DEBEN incluir al menos `timestamp` UTC, `level`, `service_name`, `correlation_id` y `message`, sin incluir secretos.
- **FR-022**: Las respuestas de API de esta feature NO DEBEN incluir campos con valor `null`; la ausencia de valor debe representarse por omision del campo.

### Constitution Alignment *(mandatory)*

- **CA-001**: Impacto por capas declarado:
  - Dominio: Propiedad, Titularidad, reglas de porcentaje y soft-delete en master data.
  - Aplicacion: casos de uso de alta, consulta, edicion, asignacion y baja logica.
  - Interfaces: contratos de entrada/salida para operaciones de propiedades y titularidad.
  - Infraestructura: persistencia y consultas de entidades de master data con auditoria.
- **CA-002**: Superficie contractual: cambiada de forma aditiva (nuevos recursos de propiedades/titularidad dentro de la version mayor vigente). No requiere incremento de version mayor mientras se mantenga retrocompatibilidad.
- **CA-003**: Si hay cambios de contrato, deben existir pruebas de contrato para crear, consultar, listar, actualizar titularidad y soft-delete, incluyendo escenarios de validacion y autenticacion.
- **CA-004**: Invariantes financieras/temporales: no se introducen eventos economicos de ledger; se aplican porcentajes 0-100 y timestamps UTC auditables.
- **CA-005**: Impacto documental: requiere actualizacion de documentacion funcional y de estado del roadmap/dependency graph cuando cambie estado del item.
- **CA-006**: Impacto TDD: implementacion funcional debe seguir ciclo rojo-verde-refactor en pruebas de dominio, aplicacion, integracion y contrato.
- **CA-007**: No se identifican nuevas reglas constitucionales sin cobertura ADR explicita para este alcance.

### Key Entities *(include if feature involves data)*

- **Propiedad**: Unidad inmobiliaria gestionable. Incluye identificador opaco, datos descriptivos y de localizacion, datos catastrales y fiscales, campos derivados, estado de borrado logico y metadatos de auditoria.
- **Titularidad**: Relacion vigente entre una propiedad y un propietario con porcentaje de participacion. Es la representacion de estado actual (sin historico de cambios de titularidad).
- **Propietario (referencia)**: Sujeto fiscal ya existente (F-0002) que puede participar en cero o mas titularidades.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un operador autenticado puede registrar una propiedad con titularidad valida en menos de 2 minutos en el flujo normal de carga.
- **SC-002**: El 100% de altas de propiedad con `type` invalido o propietario inexistente son rechazadas sin persistencia parcial.
- **SC-003**: El 100% de propiedades eliminadas logicamente deja de aparecer en consultas activas, y sus titularidades asociadas quedan marcadas como eliminadas logicamente en cascada.
- **SC-004**: El 100% de respuestas de error de la feature incluyen codigo estable, mensaje en espanol y `correlation_id`.
- **SC-005**: Al menos el 95% de consultas de listado de propiedades devuelve resultados paginados en menos de 1 segundo bajo volumen operativo esperado del contexto del sistema.
- **SC-006**: El 100% de operaciones de creacion/edicion/borrado registra metadatos de auditoria completos en UTC.

---

## Dependency Graph Impact

- **Dependencia declarada**: F-0003 depende de F-0002 en `docs/dependency-graph.yaml`; esta especificacion mantiene esa dependencia como obligatoria.
- **Consistencia detectada**: El documento fuente de feature indica "ninguna explicita", pero el DAG oficial exige dependencia con F-0002. Se toma el DAG como fuente de verdad.
- **Sin dependencias futuras**: F-0003 no introduce dependencia de items posteriores (`planned`) fuera de las ya declaradas.
- **Impacto aguas abajo**: F-0004, F-0005 y F-0006 dependen directa o indirectamente de F-0003; esta feature preserva IDs estables y reglas de titularidad para habilitarlas.
- **Sin nuevos enlaces implicitos**: No se requieren nuevos nodos ni aristas en el DAG para este alcance.

---

## ADR Gap

No se identifican gaps de ADR.

ADR materialmente impactados:

| ADR | Impacto material en F-0003 |
|-----|-----------------------------|
| ADR-0002 | Separacion de modelos y reglas de negocio de propiedad/titularidad en dominio |
| ADR-0003 | Persistencia de entidades y relaciones con auditoria y soft-delete en master data |
| ADR-0004 | Contratos HTTP resource-oriented, paginacion y disciplina de cambios aditivos |
| ADR-0005 | Requisito de autenticacion para operaciones de la feature |
| ADR-0006 | Disciplina de versionado de contratos entre roots (sin romper version mayor vigente) |
| ADR-0009 | Modelo de errores tipificados y baseline de observabilidad/correlacion |
| ADR-0011 | Representacion de porcentajes en rango 0-100 para titularidad |
| ADR-0012 | Politica temporal UTC para metadatos de auditoria |

---

## Architectural Impact

| Concern | Impact |
|---------|--------|
| HTTP Contracts | Nuevas capacidades funcionales para gestionar propiedades y titularidad. Cambio aditivo en contrato vigente. |
| Events | Sin publicacion de eventos en este slice. |
| Persistence | Nuevas entidades de master data y relacion de titularidad con auditoria, soft-delete de propiedad y soft-delete en cascada para titularidades asociadas. |
| Configuration | Sin nuevas claves de configuracion funcional requeridas. |
| Error Model | Reutiliza modelo tipificado existente (validacion, no encontrado, conflicto, no autenticado). |
| Versioning Impact | Sin ruptura de compatibilidad esperada dentro de la version mayor actual. |

---

## Out of Scope

- Operaciones de adquisicion y venta.
- Registro de hechos economicos del ledger.
- Gastos recurrentes, contratos y facturacion.
- Historico temporal de cambios de titularidad.

---

## Assumptions

- En este alcance, el total permitido para titularidad se interpreta como 100; por tanto, una suma menor se acepta (titularidad parcial) y una suma mayor se rechaza.
- Los propietarios referenciados en titularidad deben existir y estar activos al momento de asignacion.
- Campos opcionales ausentes se omiten en respuestas de API y no se serializan como `null`.

---

## Documentation Updates Required

| Document | Required Change |
|----------|-----------------|
| `docs/spec/features/F-0003-propiedades-y-titularidad.md` | Mantener alineado con decisiones de alcance y reglas finales aprobadas |
| `backend/README.md` | Documentar capacidades funcionales y reglas de uso de propiedades/titularidad cuando se implemente |
| `README.md` | Actualizar resumen de capacidades disponibles al entrar en produccion la feature |
| `docs/roadmap.md` | Actualizar estado de F-0003 (`planned` -> `in_progress` -> `done`) cuando corresponda |
| `docs/dependency-graph.yaml` | Sin cambios de dependencias; actualizar solo estado de F-0003 cuando corresponda |
