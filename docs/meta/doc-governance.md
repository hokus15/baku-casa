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
sdd/  
meta/

Cada área tiene una responsabilidad distinta.

---

## [system_docs] Documentación del sistema (`docs/system/`)

Contiene las reglas, el contexto y las convenciones globales del sistema.

Archivos principales:

| Documento | Propósito |
|---|---|
| `constitution.md` | Reglas invariantes del sistema, agnósticas al stack |
| `context.md` | Contexto operativo y alcance |
| `glossary.md` | Definiciones de términos |
| `conventions.md` | Convenciones de nomenclatura, estilo y redacción |

Reglas:

- `constitution.md` **define reglas globales**
- `context.md` **define hechos y restricciones del entorno**
- `glossary.md` **define terminología compartida**
- `conventions.md` **define forma de expresión, no invariantes ni decisiones tecnológicas**
- no deben duplicarse en specs

---

## [planning_docs] Documentación de planificación (`docs/planning/`)

Define la evolución del sistema.

Archivos principales:

| Documento | Propósito |
|---|---|
| `roadmap.md` | Evolución narrativa del sistema |
| `dependency-graph.yaml` | DAG de features y enablers |
| `item-manifest.yaml` | Contexto mínimo y punteros rápidos por item |
| `adr-map.yaml` | Fuente de verdad del mapeo item → ADR, incluyendo motivo de carga |
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
- los ADR son la fuente correcta para **elecciones tecnológicas concretas**
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

## [sdd_docs] Artefactos SDD (`docs/sdd/`)

Contiene plantillas operativas reutilizables del flujo SDD.

Reglas:

- `docs/sdd/` contiene templates de ejecución
- `docs/meta/` contiene gobierno documental y prompts auxiliares
- ambos directorios pueden evolucionar juntos, pero no deben solaparse en responsabilidad

---

## [source_of_truth_rules] Reglas de fuente de verdad

Cada tipo de información tiene un lugar único.

| Tipo de información | Documento |
|---|---|
| reglas globales del sistema | `constitution.md` |
| contexto del sistema | `context.md` |
| convenciones de nomenclatura, estilo y redacción | `conventions.md` |
| decisiones técnicas | `ADR` |
| ADRs relevantes por item y motivo de carga | `adr-map.yaml` |
| dependencias de features | `dependency-graph.yaml` |
| narrativa evolutiva | `roadmap.md` |
| comportamiento funcional | `specs/features` |
| capacidades técnicas | `specs/enablers` |
| definiciones compartidas | `specs/shared` |

`item-manifest.yaml` puede repetir un subconjunto de `adr_refs` solo como atajo operativo para resolver contexto mínimo; el mapeo canónico item → ADR vive en `adr-map.yaml`, junto con el campo `reason` que explica por qué cada ADR es materialmente relevante para el item.

La duplicación de información entre estas fuentes **debe evitarse**.

---

## [documentation_updates] Actualización de documentación

Cuando se introduce un cambio en el sistema:

1. actualizar la **spec correspondiente**
2. actualizar el **dependency graph** si cambia la estructura
3. crear o actualizar **ADR** si se toma una decisión arquitectónica
4. actualizar la **constitución** si cambian reglas globales
5. actualizar `conventions.md` si cambian reglas de nomenclatura, estilo o redacción reutilizables

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

Las decisiones tecnológicas concretas deben leerse desde ADR.

Las convenciones de nomenclatura o estilo deben leerse desde `conventions.md`.

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
