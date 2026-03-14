# Gobernanza de la Documentación — Baku.Casa

Este documento define las reglas que gobiernan la organización, mantenimiento y evolución de la documentación del proyecto.

Su objetivo es:

- mantener **fuentes de verdad claras**
- evitar **duplicación de información**
- facilitar el uso de la documentación por **personas y LLMs**
- garantizar consistencia entre documentos

---

## [documentation_principle] Principio de documentación estructurada

La documentación del sistema está organizada en **capas con responsabilidades claras**.

Cada tipo de documento tiene un propósito específico.

La información **DEBE aparecer en un único lugar**.

Los documentos **DEBEN referenciarse entre sí**, no duplicarse.

---

## [documentation_structure] Estructura de la documentación

La documentación del proyecto se organiza en el directorio `docs/`.

Estructura principal:

docs/  
system/  
planning/  
decisions/  
specs/  
meta/

Cada área tiene una responsabilidad distinta.

---

## [system_docs] Documentación del sistema (`docs/system/`)

Contiene las reglas y el contexto global del sistema.

Archivos principales:

| Documento | Propósito |
|---|---|
| `constitution.md` | Reglas invariantes del sistema |
| `context.md` | Contexto operativo y alcance |
| `glossary.md` | Definiciones de términos |
| `conventions.md` | Convenciones de nomenclatura y estilo |

Reglas:

- estos documentos **definen el sistema**
- no deben duplicarse en specs

---

## [planning_docs] Documentación de planificación (`docs/planning/`)

Define la evolución del sistema.

Archivos principales:

| Documento | Propósito |
|---|---|
| `roadmap.md` | Evolución narrativa del sistema |
| `dependency-graph.yaml` | DAG de features y enablers |
| `item-manifest.yaml` | Metadatos estructurados de items |
| `adr-map.yaml` | Relación entre items y ADR |
| `context-slices.yaml` | Conjuntos mínimos de contexto para LLM |

Reglas:

- la estructura del roadmap **vive en el dependency graph**
- el roadmap **no define dependencias**

---

## [decision_docs] Decisiones arquitectónicas (`docs/decisions/`)

Contiene **Architecture Decision Records (ADR)**.

Archivos:

docs/decisions/adr/  
docs/decisions/ADR-INDEX.md

Reglas:

- los ADR documentan **decisiones técnicas**
- las specs **pueden referenciar ADR**
- las specs **no deben redefinir decisiones ya tomadas**

---

## [spec_docs] Especificaciones (`docs/specs/`)

Contiene las especificaciones que definen el comportamiento del sistema.

Estructura:

docs/specs/  
features/  
enablers/  
shared/

### Features

Definen **comportamiento funcional observable**.

Ruta:

docs/specs/features/

### Enablers

Definen **capacidades técnicas o estructurales**.

Ruta:

docs/specs/enablers/

### Shared

Contiene definiciones reutilizables utilizadas por múltiples specs.

Ruta:

docs/specs/shared/

Reglas:

- las specs **no deben duplicar reglas de la constitución**
- las specs **deben referenciar `shared` cuando reutilicen conceptos**

---

## [meta_docs] Documentación meta (`docs/meta/`)

Contiene documentos que describen **cómo organizar la documentación y el proceso SDD**.

Ejemplos:

- taxonomía de enablers
- gobernanza documental
- plantillas de specs

Estos documentos ayudan a mantener coherencia en el proyecto.

---

## [source_of_truth_rules] Reglas de fuente de verdad

Cada tipo de información tiene un lugar único.

| Tipo de información | Documento |
|---|---|
| reglas globales del sistema | `constitution.md` |
| contexto del sistema | `context.md` |
| decisiones técnicas | `ADR` |
| dependencias de features | `dependency-graph.yaml` |
| narrativa evolutiva | `roadmap.md` |
| comportamiento funcional | `specs/features` |
| capacidades técnicas | `specs/enablers` |
| definiciones compartidas | `specs/shared` |

La duplicación de información entre estas fuentes **debe evitarse**.

---

## [documentation_updates] Actualización de documentación

Cuando se introduce un cambio en el sistema:

1. actualizar la **spec correspondiente**
2. actualizar el **dependency graph** si cambia la estructura
3. crear o actualizar **ADR** si se toma una decisión arquitectónica
4. actualizar la **constitución** si cambian reglas globales

La documentación debe evolucionar junto con el sistema.

---

## [llm_usage] Uso por LLM

La documentación está estructurada para permitir que herramientas basadas en LLM:

- carguen **contexto mínimo necesario**
- localicen información de forma determinista
- reduzcan ambigüedad

Para ello se utilizan:

- identificadores de sección
- separación clara de responsabilidades
- documentos indexados

Los LLM **no deben inferir reglas globales a partir de specs individuales**.

Las reglas globales siempre deben leerse desde `constitution.md`.

---

## [consistency_principle] Principio de consistencia documental

La documentación debe cumplir:

- **consistencia interna**
- **ausencia de duplicación**
- **claridad estructural**

Cuando exista contradicción entre documentos se aplica el siguiente orden de precedencia:

constitution.md  
> ADR  
> specification  
> implementation

Este orden debe respetarse en todo momento.