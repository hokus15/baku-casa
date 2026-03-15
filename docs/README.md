# Documentación de desarrollo

Este directorio contiene la documentación fuente de verdad para el desarrollo de **Baku.Casa** usando **SDD (Specification-Driven Development)**.

Su objetivo es:

- Centralizar la documentación relevante para diseñar, planificar e implementar la aplicación.
- Mantener una separación clara entre contexto, reglas, decisiones, planificación y especificaciones.
- Reducir el contexto necesario que se pasa a la herramienta SDD en cada fase.
- Evitar duplicidad documental y contradicciones entre artefactos.

---

## Principios del directorio `docs/`

- Cada tipo de información DEBE tener una única fuente de verdad.
- La documentación DEBE estar organizada para que una herramienta SDD pueda cargar solo el contexto mínimo necesario.
- Las reglas globales NO DEBEN repetirse dentro de specs individuales salvo referencia explícita.
- La constitución DEBE permanecer agnóstica al stack concreto.
- Las decisiones arquitectónicas relevantes DEBEN documentarse en ADRs.
- Las decisiones tecnológicas concretas NO DEBEN definirse en `system/constitution.md`.
- `system/conventions.md` NO DEBE competir con la constitución ni con los ADRs; solo define nomenclatura, estilo y forma de expresión.
- El roadmap NO DEBE actuar como fuente de verdad de dependencias técnicas.
- Las dependencias y propagación de baseline DEBEN resolverse desde el grafo y sus manifiestos asociados.

---

## Estructura

    docs/
      README.md

      system/
        constitution.md
        context.md
        glossary.md
        conventions.md

      planning/
        roadmap.md
        dependency-graph.yaml
        item-manifest.yaml
        adr-map.yaml
        context-slices.yaml

      decisions/
        adr/
        ADR-INDEX.md

      specs/
        features/
        enablers/
        shared/

      sdd/
        templates/

      meta/
        enablers-taxonomy.md
        doc-governance.md
        prompt/

---

## Responsabilidad de cada área

### system/

Contiene reglas y contexto global del sistema.

- **constitution.md**: normas obligatorias y principios invariantes, agnósticos al stack.
- **context.md**: hechos del entorno y restricciones operativas.
- **glossary.md**: definiciones compartidas.
- **conventions.md**: convenciones de nomenclatura, estilo, redacción y formato.

---

### planning/

Contiene planificación y resolución de contexto.

- **roadmap.md**: visión y secuencia funcional por MVP.
- **dependency-graph.yaml**: fuente de verdad de dependencias y orden de ejecución.
- **item-manifest.yaml**: contexto mínimo por item y referencias rápidas opcionales para resolverlo.
- **adr-map.yaml**: fuente de verdad del mapeo item → ADRs relevantes.
  Cada referencia incluye además un campo `reason` que explica por qué ese ADR debe cargarse para el item.
- **context-slices.yaml**: mapeo item/categoría → secciones relevantes de contexto y constitución.

---

### decisions/

Contiene decisiones arquitectónicas registradas.

- **adr/**: decisiones individuales.
- **ADR-INDEX.md**: índice semántico para localizar ADRs por tema o ámbito.

---

### specs/

Contiene especificaciones unitarias de trabajo.

- **features/**: features funcionales.
- **enablers/**: enablers técnicos o estructurales.
- **shared/**: reglas y catálogos compartidos para especificaciones.

---

### sdd/

Contiene templates operativos del flujo SDD.

---

### meta/

Contiene documentación de gobierno documental, clasificación auxiliar y prompts de apoyo.

---

# Fuentes de verdad

## Reglas globales

**Fuente de verdad:** `system/constitution.md`

Aquí viven las normas obligatorias del sistema:

- arquitectura  
- separación de modelos  
- reglas monetarias  
- reglas temporales  
- reglas de API  
- observabilidad  
- restricciones estructurales  
- invariantes globales  

Este documento **no debe fijar frameworks, librerías ni herramientas concretas**.

---

## Contexto operativo

**Fuente de verdad:** `system/context.md`

Aquí viven:

- dominio del sistema  
- alcance territorial  
- restricciones de despliegue  
- restricciones operativas  
- limitaciones de infraestructura  

---

## Planificación funcional

**Fuente de verdad:** `planning/roadmap.md`

Aquí vive:

- la visión por MVP  
- la agrupación de items por fase  
- el objetivo funcional de cada etapa  

---

## Dependencias y baseline técnico

**Fuente de verdad:** `planning/dependency-graph.yaml`

Aquí vive:

- el orden de ejecución  
- las dependencias entre items  
- el baseline heredado por dependencias  
- la propagación de enablers aplicables  

---

## ADRs relevantes por item

**Fuente de verdad:** `planning/adr-map.yaml`

Aquí vive:

- el conjunto canónico de ADRs materialmente relevantes por item  
- el título normalizado de cada ADR referenciado  
- el motivo de carga (`reason`) de cada ADR referenciado  

`item-manifest.yaml` puede incluir una shortlist de `adr_refs` como atajo de contexto mínimo, pero no sustituye a `adr-map.yaml`.

---

## Resolución de contexto por fase

**Fuente operativa:** `tools/resolve_sdd_context.py`

La resolución de contexto mínimo para un item y una fase SDD debe hacerse con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase <specify|clarify|plan|tasks|analyze|implement> --profile <minimal|default|deep>`

La utilidad resuelve contexto estratificado para que distintos modelos SDD consuman solo la profundidad necesaria.

### Perfiles

- `minimal`: solo contexto core del item. Recomendado para `specify` y `clarify`.
- `default`: contexto core + baseline de apoyo útil. Recomendado para `plan`, `tasks` y `analyze`.
- `deep`: contexto completo, incluyendo baseline y clausura amplia. Recomendado para `implement`.

### Significado de `core` y `supporting`

- `core`: contexto canónico y de lectura prioritaria para el item en la fase actual.
- `supporting`: contexto adicional disponible para profundizar si la fase lo necesita.

Aplicado a la salida del resolvedor:

- `core_adrs` / `core_technical_baseline`: ADRs y decisiones técnicas prioritarias.
- `supporting_adrs` / `supporting_technical_baseline`: ADRs y baseline técnico de apoyo.
- `core_constitution_sections` / `core_context_sections`: secciones explícitamente canónicas del item, declaradas en `item-manifest.yaml`.
- `supporting_constitution_sections` / `supporting_context_sections`: secciones adicionales aportadas por `context-slices.yaml`.
- `shared_specs`: contratos shared explícitos del item.
- `inherited_shared_specs`: contratos shared heredados por dependencias.
- `direct_dependencies`: baseline funcional inmediato del item.
- `transitive_dependencies`: baseline heredado del DAG.

### Regla de consumo

- Un modelo SDD debe empezar por el contexto `core`.
- Solo debe usar el contexto `supporting` cuando la fase no pueda resolverse con seguridad usando el contexto `core`.
- `deep` no implica que todo deba leerse siempre; implica que todo está disponible si hace falta profundizar.

---

## Decisiones arquitectónicas

**Fuente de verdad:** `decisions/adr/`

Aquí viven:

- decisiones técnicas relevantes  
- elecciones tecnológicas concretas  
- su racional  
- consecuencias  
- restricciones derivadas  

Los ADRs son el lugar correcto para documentar decisiones como framework HTTP, lenguaje, ORM, base de datos, estrategia de autenticación o delivery model.

---

## Convenciones de expresión

**Fuente de verdad:** `system/conventions.md`

Aquí viven:

- nomenclatura  
- estilo documental  
- formato de nombres  
- convenciones de representación no normativas  
- reglas de referencia cruzada entre documentos  

`conventions.md` **no debe redefinir invariantes globales** ni decisiones tecnológicas ya cubiertas por la constitución o por ADRs.

---

## Especificación de un item

**Fuente de verdad:** `specs/features/...` o `specs/enablers/...`

Aquí vive:

- el comportamiento o capacidad concreta del item  
- su alcance  
- sus reglas específicas  
- sus criterios de aceptación  

---

# Regla de no duplicidad

Una regla **NO DEBE** existir en más de un sitio como fuente de verdad.

Distribución esperada:

- Regla global → `constitution.md`  
- Restricción del entorno → `context.md`  
- Decisión técnica concreta → ADR  
- Convención de nomenclatura o estilo → `conventions.md`  
- Dependencia u orden → `dependency-graph.yaml`  
- ADRs relevantes por item → `adr-map.yaml`  
- Objetivo de MVP → `roadmap.md`  
- Comportamiento específico de un item → su spec  

Si una spec necesita una regla global, **DEBE referirse a ella**, no reescribirla salvo que necesite especializarla.

---

# Uso en flujo SDD

La documentación está estructurada para que la herramienta SDD no tenga que cargar todo `docs/` en cada fase.

La disciplina por fase vive en:

- `docs/sdd/templates/01_specify.md`
- `docs/sdd/templates/02_clarify.md`
- `docs/sdd/templates/03_plan.md`
- `docs/sdd/templates/04_tasks.md`
- `docs/sdd/templates/05_analyze.md`
- `docs/sdd/templates/06_implementation.md`

Resumen operativo:

- `specify` y `clarify`: resolver con perfil `minimal`
- `plan`, `tasks` y `analyze`: resolver con perfil `default`
- `implement`: resolver con perfil `deep`

---

# Objetivo de reducción de contexto

La herramienta SDD **NO DEBE recibir por defecto**:

- todos los ADRs  
- todo el roadmap  
- toda la constitución  
- todo el contexto global  
- todas las specs relacionadas  

En su lugar, el contexto **DEBE resolverse por**:

- item actual  
- closure de dependencias  
- manifiestos  
- `adr-map.yaml`  
- slices relevantes  
- ADRs mapeados  

---

# Reglas de mantenimiento

Cuando cambie una **regla global**, debe revisarse `constitution.md`.

Cuando cambie una **restricción del sistema**, debe revisarse `context.md`.

Cuando cambie una **convención de nomenclatura, estilo o redacción**, debe revisarse `conventions.md`.

Cuando cambie el **orden o baseline de ejecución**, debe revisarse `dependency-graph.yaml`.

Cuando cambie el **alcance por MVP**, debe revisarse `roadmap.md`.

Cuando una **decisión técnica tenga impacto relevante o duradero**, debe crearse o actualizarse un ADR.

Cuando una **feature o enabler cambie su comportamiento esperado**, debe actualizarse su spec.

Cuando cambie la **relevancia contextual de un item**, deben revisarse:

- `item-manifest.yaml`  
- `adr-map.yaml`  
- `context-slices.yaml`  

---

# Criterio de lectura rápida

Para entender el sistema de arriba abajo:

1. `system/context.md`  
2. `system/constitution.md`  
3. `planning/roadmap.md`  
4. `planning/dependency-graph.yaml`  
5. `decisions/ADR-INDEX.md`  
6. specs del item concreto  

---

Para trabajar un item concreto:

1. spec del item  
2. `planning/item-manifest.yaml`  
3. `planning/dependency-graph.yaml`  
4. ADRs relevantes  
5. secciones necesarias de `constitution.md` y `context.md`  

Puede resolverse automáticamente el contexto mínimo por fase con:

`python tools/resolve_sdd_context.py --item <ITEM_ID> --phase <specify|clarify|plan|tasks|analyze|implement> --profile <minimal|default|deep>`

---

# Estado esperado

Este directorio debe permitir que cualquier trabajo de **diseño, planificación o implementación** pueda resolverse con:

- contexto mínimo  
- autoridad documental clara  
- baja redundancia  
- alta trazabilidad  
- bajo riesgo de contradicción
