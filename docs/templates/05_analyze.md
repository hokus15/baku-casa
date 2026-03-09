# Spec-Kit Prompt Template — `/speckit.analyze`

Analiza el Roadmap Item **<ID> - <Título>** y su documentación asociada para evaluar su **coherencia, consistencia y alineación con el sistema** antes de iniciar `/speckit.specify`.

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

El objetivo es verificar que el Roadmap Item esté **correctamente definido dentro del sistema**, alineado con el roadmap y compatible con las decisiones arquitectónicas del proyecto.

Al trabajar sobre una Feature, debes tratar como baseline del sistema todos los Enablers previos aplicables marcados en `docs/dependency-graph.yaml` con `affects_future_features: true`, aunque no aparezcan repetidos explícitamente en la descripción de la Feature.

---

# Fuentes Autoritativas

Debes basar el análisis exclusivamente en:

- `docs/constitution.md`
- `docs/context.md`
- `docs/roadmap.md`
- `docs/dependency-graph.yaml`
- `docs/spec/features/<feature-file>.md` (si es Feature)
- `docs/spec/enablers/<enabler-file>.md` (si es Enabler)
- `docs/enablers-taxonomy.md`
- `docs/adr/ADR-0001..ADR-0014`

El análisis **no puede contradecir ninguno de estos documentos**.

---

# Disciplina del Dependency Graph

El roadmap está definido como un **DAG de dependencias** en:

`docs/dependency-graph.yaml`

Debes comprobar que el Roadmap Item:

- tenga dependencias coherentes con su propósito
- no dependa de Features o Enablers posteriores en el roadmap
- no introduzca dependencias implícitas no declaradas
- esté correctamente ubicado en la secuencia de implementación

Si detectas inconsistencias debes indicarlo en:

```
Dependency Graph Issue
```

---

# Disciplina de ADR

Debes verificar que el Roadmap Item sea **compatible con todos los ADR vigentes**.

Debes identificar posibles conflictos con decisiones arquitectónicas existentes.

Si detectas que el item requeriría crear o modificar un ADR debes indicarlo en:

```
ADR Gap
```

---

# Consistencia con la Constitución

Debes comprobar que el Roadmap Item sea compatible con las reglas definidas en:

`docs/constitution.md`

Especialmente en aspectos como:

- modelo de dinero
- representación de porcentajes
- disciplina temporal (UTC)
- modelo de errores
- reglas del dominio económico

---

# Consistencia del Roadmap

Debes comprobar que el Roadmap Item:

- esté alineado con los objetivos del sistema
- tenga sentido dentro de la evolución del roadmap
- respete la separación entre Features y Enablers
- no introduzca capacidades fuera del alcance actual del proyecto

---

# Impacto en el Sistema

Debes identificar si el Roadmap Item probablemente afectará:

- contratos HTTP
- eventos
- persistencia
- configuración
- modelo de errores

El objetivo es anticipar áreas del sistema que podrían verse impactadas por la implementación.

---

# Consistencia de Documentación

Debes comprobar si existe alguna inconsistencia entre:

- `docs/roadmap.md`
- `docs/dependency-graph.yaml`
- la documentación del Roadmap Item

Si detectas desalineaciones debes indicarlo.

---

# Dependency Awareness

Debes analizar `docs/dependency-graph.yaml` antes de generar el resultado.

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

- `docs/roadmap.md`
- `docs/dependency-graph.yaml`
- `docs/constitution.md`
- `docs/adr/ADR-0001..ADR-0014`

No debes limitar el análisis a dependencias directas ni a la Feature actual.

Solo deben actualizarse Features ya existentes en `docs/spec/features/`. No deben anticiparse ni inventarse cambios en Features aún no definidas documentalmente.

## Dependencias transitivas

Debes considerar no solo dependencias directas, sino también dependencias transitivas a través de toda la cadena del DAG.

## Consistencia de estado

Debes tomar como fuente de verdad el estado declarado en `docs/dependency-graph.yaml`.

Estados permitidos:

- `planned`
- `in_progress`
- `done`

---

# Restricciones

Durante el análisis **NO debes**:

- diseñar la solución
- proponer implementación técnica
- modificar ADR existentes
- introducir tecnologías o frameworks
- redefinir la Feature o Enabler