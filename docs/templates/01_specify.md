# Spec-Kit Prompt Template — `/speckit.specify`

Genera la **especificación** para el Roadmap Item **<ID>**: "**<Título>**".

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

La especificación debe definir **el comportamiento esperado del sistema** respetando las reglas del proyecto y sin introducir decisiones de implementación.

---

# Fuentes Autoritativas

Debes basar la especificación exclusivamente en:

- `docs/spec/constitution.md`
- `docs/spec/context.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- `docs/spec/features/<feature-file>.md` (si es Feature)
- `docs/spec/enablers/<enabler-file>.md` (si es Enabler)
- `docs/spec/enablers-taxonomy.md`
- `docs/adr/ADR-0001..ADR-0014`

La especificación **no puede contradecir ninguno de estos documentos**.

---

# Disciplina del Dependency Graph

El roadmap está definido como un **DAG de dependencias** en:

`docs/spec/dependency-graph.yaml`

Debes comprobar que el Roadmap Item:

- respete las dependencias declaradas
- no requiera Features o Enablers posteriores en el roadmap
- no introduzca dependencias implícitas no declaradas

Si detectas inconsistencias debes indicarlo en:

```
Dependency Graph Impact
```

---

# Disciplina de ADR

La especificación debe respetar **todos los ADR vigentes**.

Solo deben mencionarse explícitamente los **ADR materialmente impactados** por este Roadmap Item.

Si detectas que la Feature o Enabler requiere crear o modificar un ADR debes indicarlo en:

```
ADR Gap
```

---

# Consistencia con la Constitución

La especificación debe respetar las reglas definidas en:

`docs/spec/constitution.md`

Especialmente en aspectos como:

- representación de dinero
- porcentajes
- disciplina temporal (UTC)
- modelo de errores
- reglas del dominio económico

---

# Consistencia del Roadmap

Debes comprobar que el Roadmap Item:

- tenga sentido dentro del roadmap
- esté alineado con el contexto del sistema
- respete la separación entre Features y Enablers

---

# Impactos Arquitectónicos

Debes identificar si el Roadmap Item introduce o modifica:

- contratos HTTP
- eventos
- persistencia
- configuración
- modelo de errores

Si existen cambios contractuales o eventos debe indicarse el **impacto en versionado**.

---

# Actualización y Sincronización de Documentación

La especificación debe identificar si el Roadmap Item requiere actualizar documentación existente.

Debes considerar cuando corresponda:

- `backend/README.md`
- `bot/README.md`
- `frontend/README.md`
- `README.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

---

## Sincronización de estado del roadmap

Si la especificación cambia el estado del item, debe indicarse la necesidad de actualizar de forma consistente:

- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

Estados permitidos:

- `planned`
- `in_progress`
- `done`

---

# Restricciones

La especificación **NO debe**:

- describir implementación
- introducir frameworks o tecnologías
- definir estructura de código
- introducir decisiones arquitectónicas que contradigan ADR