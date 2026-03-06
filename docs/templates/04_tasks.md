# Spec-Kit Prompt Template — `/speckit.tasks`

Genera las **tareas de implementación** para el Roadmap Item **<ID>**: "**<Título>**".

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

Las tareas deben derivar directamente del **plan generado por `/speckit.plan`** para este item.

---

# Fuentes Autoritativas

Debes basarte exclusivamente en:

- `docs/spec/constitution.md`
- `docs/spec/context.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- `docs/spec/features/<feature-file>.md` (si es Feature)
- `docs/spec/enablers/<enabler-file>.md` (si es Enabler)
- `docs/spec/enablers-taxonomy.md`
- `docs/adr/ADR-0001..ADR-0014`
- el resultado generado por `/speckit.plan` para este item

Las tareas **no pueden contradecir ninguno de estos documentos**.

---

# Disciplina del Dependency Graph

El roadmap está definido como un **DAG de dependencias** en:

`docs/spec/dependency-graph.yaml`

Debes:

- respetar las dependencias declaradas
- asegurar que ninguna tarea dependa de Features o Enablers aún no implementados
- mantener un orden de tareas compatible con el DAG

Si detectas inconsistencias debes indicarlo en:

```
Dependency Graph Issue
```

---

# Disciplina Arquitectónica

Todas las tareas deben respetar **los ADR vigentes**.

Las tareas deben reflejar el cumplimiento de:

- arquitectura hexagonal
- disciplina de persistencia
- disciplina de eventos
- modelo de errores
- versionado de contratos

No deben introducir decisiones arquitectónicas que contradigan los ADR.

---

# Cobertura de Implementación

Las tareas deben cubrir todas las áreas necesarias para implementar el item según el plan, incluyendo cuando corresponda:

- dominio
- servicios de aplicación
- persistencia
- interfaces (HTTP o eventos)
- integración entre componentes
- tests
- wiring de dependencias

No se deben generar migraciones concretas ni código.

---

# Actualización y Sincronización de Documentación

Las tareas deben incluir explícitamente las acciones necesarias para **mantener la documentación sincronizada con la implementación**.

Debes considerar cuando corresponda:

- `backend/README.md`
- `bot/README.md`
- `frontend/README.md`
- `README.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

---

## Sincronización de estado del roadmap

Si la implementación cambia el estado del item, debe existir una tarea para actualizar de forma consistente:

- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

Estados permitidos:

- `planned`
- `in_progress`
- `done`

---

# Restricciones

Las tareas **NO deben**:

- introducir nuevas decisiones arquitectónicas
- modificar ADR existentes
- introducir tecnologías no definidas por los ADR
- redefinir la especificación funcional