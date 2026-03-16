# F-0013: Tareas

---

## Objetivo

Gestionar tareas operativas dirigidas al propietario, permitiendo registrar acciones pendientes derivadas de eventos del sistema o creadas manualmente, y facilitar su ejecución mediante un contexto asociado.

---

## Alcance

Esta feature cubre:

- Crear tareas manualmente
- Crear tareas automáticamente desde otras features
- Consultar detalle de tarea (incluyendo contexto)

---

## Fuera de alcance

- Implementación concreta de envío de notificaciones (WhatsApp, email, etc.)
- Implementación concreta de generación de documentos
- Motor de workflows

---

## Definiciones

**Tarea**: elemento accionable que representa una acción pendiente o realizada por el propietario.

- Las tareas pueden ser generadas por el sistema o creadas manualmente por el propietario.
- Todas las tareas están destinadas al propietario (no existe asignación a usuarios).

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Tarea
- Ver definiciones de dominio y datos principales de la feature

---

## Datos principales

La feature gestiona la siguiente información:

### Datos de la tarea

### Identificación

- `task_id`

---

### Estado

Estado de la tarea (lista cerrada):

- PENDIENTE
- FINALIZADA
- SALTADA

---

### Fechas

- `creation_date`
- `due_date`
- `completion_date` (opcional; requerida si estado = FINALIZADA)

---

### Prioridad

Prioridad informativa (lista cerrada):

- BAJA
- MEDIA
- ALTA

La prioridad no tiene impacto funcional por ahora (solo informativa).

---

### Tipo de tarea

Define el propósito de la tarea y determina las acciones disponibles.

Lista abierta gobernada por las features que producen tareas.

`F-0013` define el contenedor común (`task_type`, estado, contexto y ciclo de vida), pero no impone un catálogo cerrado global.

Ejemplos:

- NOTIFICAR_ACTUALIZACION_RENTA
- GENERAR_DOCUMENTO
- RECORDATORIO
- REVISION_CONTRATO

---

### Contexto

La tarea contiene un contexto estructurado y extensible con la información necesaria para ejecutar acciones asociadas.

El contexto debe permitir almacenar pares clave-valor o una estructura equivalente que preserve datos compuestos de forma estable.

Ejemplos de datos posibles:

- `rent_update_id`
- `contract_id`
- `tenant_phone`
- `document_template_id`
- `property_id`

El contexto no contiene lógica, solo datos necesarios para ejecutar acciones.

---

### Auditoría

Esta feature reutiliza el contrato común de auditoría definido en:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md

---

### Acciones de tarea

Las acciones que se pueden realizar sobre una tarea no están definidas por el sistema.

El cliente que consume la tarea es responsable de interpretar su tipo y contexto y decidir qué acciones ofrece al usuario.

El sistema únicamente expone:

- estado de la tarea
- tipo de tarea
- contexto
- fechas

---

## Capacidades

El sistema debe permitir:

- Crear tareas manualmente
- Crear tareas automáticamente desde otras features
- Consultar detalle de tarea (incluyendo contexto)
- Listar tareas
- Filtrar tareas por estado
- Consultar tareas no cerradas (estado = PENDIENTE)
- Filtrar tareas por fecha límite
- Cambiar estado de tarea
- Reabrir tareas
- Los listados y consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Reglas del dominio

- Toda tarea debe tener un estado.
- Una tarea en estado FINALIZADA debe tener `completion_date`.
- Una tarea en estado SALTADA no requiere `completion_date`.
- El sistema no valida la semántica del contexto.
- El cliente es responsable de interpretar el tipo de tarea y su contexto.
- Las tareas no tienen múltiples fechas límite.
- Las tareas generadas automáticamente deben incluir una identidad de idempotencia en su contexto (`automation_key`) siguiendo el contrato común definido en docs/specs/shared/SHARED-0005-idempotency-contract.md

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Toda tarea debe tener un estado.
- Una tarea en estado FINALIZADA debe tener `completion_date`.
- Una tarea en estado SALTADA no requiere `completion_date`.

---

## Dependencias

Esta feature puede depender de:

- F-0012

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0001-audit-and-soft-delete.md
- docs/specs/shared/SHARED-0002-pagination-contract.md
- docs/specs/shared/SHARED-0005-idempotency-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- Crear tareas manualmente
- Crear tareas automáticamente desde otras features
- Consultar detalle de tarea (incluyendo contexto)
