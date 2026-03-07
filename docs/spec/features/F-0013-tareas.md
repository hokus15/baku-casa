# F-0013: Tareas

## Objetivo

Gestionar tareas operativas dirigidas al propietario, permitiendo registrar acciones pendientes derivadas de eventos del sistema o creadas manualmente, y facilitar su ejecución mediante un contexto asociado.

---

## Definiciones

**Tarea**: elemento accionable que representa una acción pendiente o realizada por el propietario.

- Las tareas pueden ser generadas por el sistema o creadas manualmente por el propietario.
- Todas las tareas están destinadas al propietario (no existe asignación a usuarios).

---

## Datos de la tarea

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

- `fecha_creacion`
- `fecha_limite`
- `fecha_finalizacion` (opcional; requerida si estado = FINALIZADA)

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

Lista abierta dependiente de implementación.

Ejemplos:

- NOTIFICAR_ACTUALIZACION_RENTA
- GENERAR_DOCUMENTO
- RECORDATORIO
- REVISION_CONTRATO

---

### Contexto

La tarea contiene un contexto estructurado y extensible con la información necesaria para ejecutar acciones asociadas.

El contexto debe permitir almacenar pares clave-valor o estructura JSON equivalente.

Ejemplos de datos posibles:

- `rent_update_id`
- `contract_id`
- `tenant_phone`
- `document_template_id`
- `property_id`

El contexto no contiene lógica, solo datos necesarios para ejecutar acciones.

---

### Auditoría

- `created_at`
- `created_by`
- `updated_at`
- `updated_by`

---

## Acciones de tarea

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

---

## Reglas de negocio

- Toda tarea debe tener un estado.
- Una tarea en estado FINALIZADA debe tener `fecha_finalizacion`.
- Una tarea en estado SALTADA no requiere `fecha_finalizacion`.
- El sistema no valida la semántica del contexto.
- El cliente es responsable de interpretar el tipo de tarea y su contexto.
- Las tareas no tienen múltiples fechas límite.
- Las tareas generadas automáticamente deben incluir una clave de idempotencia en su contexto (`automation_key`) para evitar duplicados.
- Las tareas automáticas deben incluir automation_key en el contexto para idempotencia.

---

## Fuera de alcance

- Implementación concreta de envío de notificaciones (WhatsApp, email, etc.)
- Implementación concreta de generación de documentos
- Motor de workflows

---

---

## Dependencias y trazabilidad

### Depende de
- (ninguna explícita)

### Impacto en contratos
- HTTP API: (si aplica)
- Eventos (CloudEvents): (si aplica)

---

## ADR aplicables

### Base
- ADR-0001
- ADR-0002
- ADR-0003
- ADR-0004
- ADR-0005
- ADR-0006
- ADR-0007
- ADR-0008
- ADR-0009
- ADR-0011
- ADR-0012

### Condicionales
- ADR-0010 (si esta feature publica/consume eventos con entrega duradera)


---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Correlacion por request mediante `correlation_id`.
