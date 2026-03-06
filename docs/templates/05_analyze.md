# Spec-Kit Prompt Template — `/speckit.analyze`

Analiza el Roadmap Item **<ID>**: "**<Título>**" y su documentación asociada para evaluar su **coherencia, consistencia y alineación con el sistema** antes de iniciar `/speckit.specify`.

El item puede ser:

- Feature (F-XXXX)
- Enabler (EN-XXXX)

El objetivo es verificar que el Roadmap Item esté **correctamente definido dentro del sistema**, alineado con el roadmap y compatible con las decisiones arquitectónicas del proyecto.

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

El análisis **no puede contradecir ninguno de estos documentos**.

---

# Disciplina del Dependency Graph

El roadmap está definido como un **DAG de dependencias** en:

`docs/spec/dependency-graph.yaml`

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

`docs/spec/constitution.md`

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

- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- la documentación del Roadmap Item

Si detectas desalineaciones debes indicarlo.

---

# Restricciones

Durante el análisis **NO debes**:

- diseñar la solución
- proponer implementación técnica
- modificar ADR existentes
- introducir tecnologías o frameworks
- redefinir la Feature o Enabler