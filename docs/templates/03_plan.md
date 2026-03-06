# Spec-Kit Prompt Template — `/speckit.plan`

Genera el **plan de implementación** para el Roadmap Item **<ID> - <Título>**.

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

El plan debe describir **cómo se implementará la especificación respetando la arquitectura y las decisiones definidas en los ADR**.

Al trabajar sobre una Feature, debes tratar como baseline del sistema todos los Enablers previos aplicables marcados en `docs/spec/dependency-graph.yaml` con `affects_future_features: true`, aunque no aparezcan repetidos explícitamente en la descripción de la Feature.

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

# Dependency Awareness

Debes analizar `docs/spec/dependency-graph.yaml` antes de generar el resultado.

## Enablers ya existentes

Si el Roadmap Item es una Feature, debes identificar todos los Enablers con estado `done` o `in_progress` que ya formen parte del sistema y determinar cuáles le aplican directa o indirectamente según el dependency graph.

La Feature debe asumir que esos Enablers ya existen y debe integrarse con ellos cuando sea aplicable.

No debes:

- ignorar Enablers ya implementados
- redefinir capacidades ya cubiertas por Enablers existentes
- duplicar responsabilidades técnicas ya introducidas por otros Roadmap Items

## Impacto de Enablers sobre Features existentes

Si el Roadmap Item es un Enabler, debes identificar todas las Features existentes en `docs/spec/features/` que dependan de este Enabler, directa o indirectamente, a través de toda la cadena de dependencias del dependency graph.

Para cada Feature afectada debes reflejar los cambios necesarios en su especificación para integrar correctamente el Enabler, manteniendo coherencia con:

- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- `docs/spec/constitution.md`
- `docs/adr/ADR-0001..ADR-0014`

No debes limitar el análisis a dependencias directas ni a la Feature actual.

Solo deben actualizarse Features ya existentes en `docs/spec/features/`. No deben anticiparse ni inventarse cambios en Features aún no definidas documentalmente.

## Dependencias transitivas

Debes considerar no solo dependencias directas, sino también dependencias transitivas a través de toda la cadena del DAG.

## Consistencia de estado

Debes tomar como fuente de verdad el estado declarado en `docs/spec/dependency-graph.yaml`.

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