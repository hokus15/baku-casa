# Spec-Kit Prompt Template — `/speckit.clarify`

Analiza la especificación del Roadmap Item **<ID> - <Título>** e identifica **ambigüedades, inconsistencias o definiciones incompletas** que deban resolverse antes de continuar con `/speckit.plan`.

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

El objetivo es garantizar que la especificación sea **suficientemente clara, consistente y completa** para permitir implementaciones reproducibles.

Al trabajar sobre una Feature, debes tratar como baseline del sistema todos los Enablers previos aplicables marcados en `docs/spec/dependency-graph.yaml` con `affects_future_features: true`, aunque no aparezcan repetidos explícitamente en la descripción de la Feature.

---

# Fuentes Autoritativas

Debes basar el análisis exclusivamente en:

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

Debes comprobar que la especificación:

- sea consistente con sus dependencias declaradas
- no requiera Features o Enablers posteriores en el roadmap
- no introduzca dependencias implícitas no declaradas

Si detectas problemas debes indicarlo en:

```
Dependency Graph Issue
```

---

# Disciplina de ADR

Debes verificar que la especificación:

- respete todos los ADR vigentes
- no contradiga decisiones arquitectónicas existentes

Solo debes mencionar ADR cuando exista:

- posible conflicto
- ambigüedad respecto a un ADR
- necesidad de crear o modificar un ADR

Si detectas este último caso debes indicarlo en:

```
ADR Gap
```

---

# Consistencia con la Constitución

Debes comprobar que la especificación respete las reglas definidas en:

`docs/spec/constitution.md`

Especialmente en aspectos como:

- representación de dinero
- porcentajes
- disciplina temporal (UTC)
- modelo de errores
- reglas del dominio económico

Si detectas inconsistencias debes indicarlo explícitamente.

---

# Consistencia del Roadmap

Debes comprobar que la Feature o Enabler:

- tenga sentido dentro del roadmap
- esté alineada con el contexto del sistema
- no introduzca capacidades fuera del alcance del roadmap actual

---

# Impacto en Documentación

Debes identificar si la especificación podría requerir cambios o aclaraciones en:

- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- `docs/spec/context.md`
- `docs/spec/constitution.md`

Si detectas inconsistencias o falta de alineación debes indicarlo.

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

Durante el proceso de clarificación **NO debes**:

- proponer implementación técnica
- introducir decisiones de arquitectura nuevas
- modificar ADR existentes
- introducir tecnologías o frameworks
- rediseñar la Feature o Enabler

El objetivo es **aclarar la especificación**, no diseñar la implementación.