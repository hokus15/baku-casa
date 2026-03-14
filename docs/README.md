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
- Las decisiones arquitectónicas relevantes DEBEN documentarse en ADRs.
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

---

## Responsabilidad de cada área

### system/

Contiene reglas y contexto global del sistema.

- **constitution.md**: normas obligatorias y principios invariantes.
- **context.md**: hechos del entorno y restricciones operativas.
- **glossary.md**: definiciones compartidas.
- **conventions.md**: convenciones transversales de diseño y desarrollo.

---

### planning/

Contiene planificación y resolución de contexto.

- **roadmap.md**: visión y secuencia funcional por MVP.
- **dependency-graph.yaml**: fuente de verdad de dependencias y orden de ejecución.
- **item-manifest.yaml**: contexto mínimo por item.
- **adr-map.yaml**: mapeo item → ADRs relevantes.
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

Contiene prompts, templates y artefactos auxiliares del flujo SDD.

---

### meta/

Contiene documentación de gobierno documental y clasificación auxiliar.

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
- testing  
- errores  
- invariantes globales  

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

## Decisiones arquitectónicas

**Fuente de verdad:** `decisions/adr/`

Aquí viven:

- decisiones técnicas relevantes  
- su racional  
- consecuencias  
- restricciones derivadas  

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
- Dependencia u orden → `dependency-graph.yaml`  
- Objetivo de MVP → `roadmap.md`  
- Comportamiento específico de un item → su spec  

Si una spec necesita una regla global, **DEBE referirse a ella**, no reescribirla salvo que necesite especializarla.

---

# Uso en flujo SDD

La documentación está estructurada para que la herramienta SDD no tenga que cargar todo `docs/` en cada fase.

---

## Specify

Debe cargar como mínimo:

- spec del item  
- `item-manifest.yaml` del item  
- dependencias relevantes  
- ADRs relevantes  
- secciones relevantes de `constitution.md` y `context.md`  

---

## Plan

Debe cargar como mínimo:

- spec aprobada del item  
- manifiesto del item  
- dependencias relevantes  
- ADRs relevantes  
- reglas globales aplicables  

---

## Implement

Debe cargar como mínimo:

- spec  
- plan  
- tasks  
- ADRs relevantes  
- reglas globales aplicables  
- dependencias técnicas necesarias  

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
- slices relevantes  
- ADRs mapeados  

---

# Reglas de mantenimiento

Cuando cambie una **regla global**, debe revisarse `constitution.md`.

Cuando cambie una **restricción del sistema**, debe revisarse `context.md`.

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

---

# Estado esperado

Este directorio debe permitir que cualquier trabajo de **diseño, planificación o implementación** pueda resolverse con:

- contexto mínimo  
- autoridad documental clara  
- baja redundancia  
- alta trazabilidad  
- bajo riesgo de contradicción