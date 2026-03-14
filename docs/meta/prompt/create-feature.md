# Prompt — Crear especificación de Feature

## Objetivo

Generar una nueva **especificación de Feature** para el proyecto Baku.Casa.

La feature describe **comportamiento funcional del sistema observable por el usuario o por otros sistemas**.

El resultado debe seguir la estructura definida en:

docs/specs/templates/feature-template.md

---

## Contexto

Baku.Casa sigue el modelo **Specification Driven Development (SDD)**.

La documentación del sistema está organizada en:

docs/system/  
docs/planning/  
docs/decisions/  
docs/specs/  
docs/meta/

Documentos relevantes:

docs/system/constitution.md  
docs/system/context.md  
docs/system/glossary.md  
docs/meta/enablers-taxonomy.md  
docs/planning/dependency-graph.yaml  
docs/specs/templates/feature-template.md  
docs/specs/shared/

---

## Idioma

La especificación generada debe escribirse **en castellano**.

---

## Instrucciones

1. Identificar la **capacidad funcional del dominio** que introduce la feature.

2. Determinar las **entidades de dominio principales** implicadas.

3. Generar la especificación usando el template de feature:

docs/specs/templates/feature-template.md

4. Rellenar todos los placeholders:

{{FIELD_NAME}}

5. Eliminar todos los bloques de instrucción:

<<INSTRUCTION>>
...
<<END_INSTRUCTION>>

El documento final **NO debe contener placeholders ni bloques de instrucción**.

---

## Reglas

La feature generada:

- DEBE introducir **comportamiento funcional del dominio**
- DEBE describir **comportamiento observable**
- DEBE respetar las reglas definidas en:

docs/system/constitution.md

- NO DEBE introducir decisiones técnicas de implementación
- NO DEBE redefinir decisiones arquitectónicas documentadas en ADR
- NO DEBE describir estructuras de base de datos
- NO DEBE describir frameworks o tecnologías

Las dependencias **NO deben inventarse**.

Las dependencias se definen exclusivamente en:

docs/planning/dependency-graph.yaml

---

## Uso de shared specs

Cuando una feature reutilice conceptos comunes, debe referenciar:

docs/specs/shared/

Ejemplos típicos:

- modelos de dominio compartidos
- reglas de dinero o porcentajes
- modelos temporales
- contratos API

La feature **NO debe duplicar definiciones ya presentes en shared**.

---

## Reglas del dominio

Las reglas del dominio deben:

- describir invariantes del negocio
- definir comportamiento del sistema
- ser independientes de la implementación

Las reglas **NO deben describir código o arquitectura técnica**.

---

## Casos borde

La feature debe considerar situaciones límite del dominio, por ejemplo:

- estados inconsistentes
- operaciones repetidas
- valores extremos
- ausencia de datos esperados

Estos casos deben describirse a nivel de **comportamiento del sistema**.

---

## Criterios de aceptación

Los criterios de aceptación deben describir **resultados observables**, por ejemplo:

- la operación produce el estado esperado
- el sistema aplica correctamente las reglas del dominio
- los datos generados son coherentes con el modelo del sistema

Los criterios **NO deben describir implementación técnica**.

---

## Salida esperada

Devolver **únicamente el documento Markdown final** de la especificación de la feature.

No incluir explicaciones ni comentarios.

El resultado debe poder guardarse directamente como:

docs/specs/features/F-XXXX-nombre.md

## Idioma

La especificación generada debe escribirse en **castellano**.