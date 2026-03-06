# Spec-Kit Prompt Template — `/speckit.plan`

Genera el **plan de implementación** para el Roadmap Item **<ID>**: "**<Título>**".

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

El plan debe describir **cómo se implementará la especificación respetando la arquitectura y las decisiones definidas en los ADR**.

---

# Fuentes Autoritativas

Debes basar el plan exclusivamente en:

- `docs/spec/constitution.md`
- `docs/spec/context.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- `docs/spec/features/<feature-file>.md` (si es Feature)
- `docs/spec/enablers/<enabler-file>.md` (si es Enabler)
- `docs/spec/enablers-taxonomy.md`
- `docs/adr/ADR-0001..ADR-0014`

El plan **no puede contradecir ninguno de estos documentos**.

---

# Disciplina del Dependency Graph

El roadmap está definido como un **DAG de dependencias** en:

`docs/spec/dependency-graph.yaml`

Debes comprobar que:

- todas las dependencias del item estén satisfechas
- el orden de implementación sea consistente con el DAG
- el item no requiera Features o Enablers posteriores en el roadmap

Si detectas inconsistencias debes indicarlo en:

```
Dependency Graph Issue
```

---

# Disciplina de ADR

El plan debe respetar **todos los ADR vigentes**.

Debes identificar los **ADR materialmente impactados** por este Roadmap Item y explicar cómo la implementación respetará dichas decisiones.

Si detectas que la implementación requiere crear o modificar un ADR debes indicarlo en:

```
ADR Gap
```

---

# Impactos Arquitectónicos

Debes identificar si el item introduce o modifica:

- contratos HTTP
- eventos
- persistencia
- configuración
- modelo de errores

Si existen cambios contractuales o de eventos debes indicar el **impacto en versionado**.

---

# Consistencia con la Constitución

Debes comprobar que el plan respete las reglas definidas en:

`docs/spec/constitution.md`

Especialmente en aspectos como:

- representación de dinero
- porcentajes
- disciplina temporal (UTC)
- modelo de errores
- reglas del dominio económico

---

# Consistencia del Roadmap

Debes comprobar que el plan:

- esté alineado con el roadmap
- no introduzca capacidades fuera del alcance del roadmap actual
- respete la separación entre Features y Enablers

---

# Actualización y Sincronización de Documentación

El plan debe identificar la documentación que deberá actualizarse como parte de la implementación.

Debes considerar cuando corresponda:

- `backend/README.md`
- `bot/README.md`
- `frontend/README.md`
- `README.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

---

## Sincronización de estado del roadmap

Si la implementación cambia el estado del item, el plan debe indicar la necesidad de actualizar de forma consistente:

- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`

Estados permitidos:

- `planned`
- `in_progress`
- `done`

---

# Restricciones

El plan **NO debe**:

- incluir código
- generar migraciones concretas
- repetir la especificación funcional
- introducir decisiones arquitectónicas que contradigan ADR
- introducir tecnologías no definidas por los ADR