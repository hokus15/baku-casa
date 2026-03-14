# Prompt — Crear especificación de Enabler

## Objetivo

Generar una nueva **especificación de Enabler** para el proyecto Baku.Casa.

El resultado debe seguir la estructura definida en:

docs/specs/templates/enabler-template.md

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
docs/meta/enablers-taxonomy.md  
docs/planning/dependency-graph.yaml  
docs/specs/templates/enabler-template.md

---

## Instrucciones

1. Identificar la **capacidad técnica** que introduce el enabler.

2. Clasificar el enabler según la taxonomía definida en:

docs/meta/enablers-taxonomy.md

3. Generar la especificación usando el template de enabler.

4. Rellenar todos los placeholders:

{{FIELD_NAME}}

5. Eliminar todos los bloques de instrucción:

<<INSTRUCTION>>
...
<<END_INSTRUCTION>>

El documento final **NO debe contener placeholders ni bloques de instrucción**.

---

## Reglas

El enabler generado:

- DEBE introducir **una capacidad técnica**
- NO DEBE introducir funcionalidad de dominio
- NO DEBE redefinir decisiones arquitectónicas ya documentadas en ADR
- NO DEBE describir detalles de implementación
- DEBE describir la capacidad en términos de **comportamiento del sistema**

Las dependencias **NO deben inventarse**.

Las dependencias se definen exclusivamente en:

docs/planning/dependency-graph.yaml

---

## Criterios de aceptación

Los criterios de aceptación deben describir **resultados observables**, por ejemplo:

- la capacidad técnica está disponible en el sistema
- la arquitectura mantiene consistencia con la constitución
- las features futuras pueden utilizar la capacidad introducida

Los criterios **NO deben describir implementación técnica**.

---

## Salida esperada

Devolver **únicamente el documento Markdown final** de la especificación del enabler.

No incluir explicaciones ni comentarios.

El resultado debe poder guardarse directamente como:

docs/specs/enablers/EN-XXXX-nombre.md

## Idioma

La especificación generada debe escribirse en **castellano**.