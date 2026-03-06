# Spec-Kit Prompt Template — `/speckit.implement`

Implementa el Roadmap Item **<ID>**: "**<Título>**" siguiendo las **tareas generadas por `/speckit.tasks`**.

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

La implementación debe seguir estrictamente el **plan generado por `/speckit.plan`** y respetar todas las decisiones arquitectónicas del proyecto.

---

# Fuentes Autoritativas

Debes basar la implementación exclusivamente en:

- `docs/spec/constitution.md`
- `docs/spec/context.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- `docs/spec/features/<feature-file>.md` (si es Feature)
- `docs/spec/enablers/<enabler-file>.md` (si es Enabler)
- `docs/spec/enablers-taxonomy.md`
- `docs/adr/ADR-0001..ADR-0014`
- el resultado de `/speckit.plan`
- el resultado de `/speckit.tasks`

La implementación **no puede contradecir ninguno de estos documentos**.

---

# Disciplina del Dependency Graph

El roadmap está definido como un **DAG de dependencias** en:

`docs/spec/dependency-graph.yaml`

Debes comprobar que:

- todas las dependencias del item estén satisfechas antes de implementar
- la implementación no introduzca dependencias nuevas no declaradas
- el orden de ejecución sea compatible con el DAG

Si detectas inconsistencias debes indicarlo en:

```
Dependency Graph Issue
```

---

# Disciplina de ADR

La implementación debe respetar **todos los ADR vigentes**.

Debes asegurarte de que la implementación cumpla las decisiones arquitectónicas establecidas.

Si durante la implementación detectas que sería necesario crear o modificar un ADR debes indicarlo en:

```
ADR Gap
```

---

# Consistencia con la Constitución

La implementación debe respetar las reglas definidas en:

`docs/spec/constitution.md`

Especialmente en aspectos como:

- representación de dinero
- porcentajes
- disciplina temporal (UTC)
- modelo de errores
- reglas del dominio económico

---

# Consistencia con el Plan y las Tareas

Debes implementar siguiendo:

- el plan de implementación
- las tareas generadas

Si detectas inconsistencias entre **spec, plan o tasks**, debes indicarlo antes de continuar.

---

# Actualización y Sincronización de Documentación

Durante la implementación debes mantener la documentación sincronizada con el estado real del sistema.

Debes actualizar cuando corresponda:

- `backend/README.md`
- `bot/README.md`
- `frontend/README.md`
- `README.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

---

## Sincronización de estado del roadmap

Si el Roadmap Item cambia de estado, debes actualizar de forma consistente:

- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

Estados permitidos:

- `planned`
- `in_progress`
- `done`

---

# Restricciones

La implementación **NO debe**:

- introducir decisiones arquitectónicas que contradigan ADR
- introducir tecnologías no definidas en los ADR
- modificar ADR existentes
- modificar la especificación funcional sin pasar por `/speckit.specify`