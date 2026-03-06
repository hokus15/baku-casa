# Templates — Spec-Driven Development Prompts

Esta carpeta contiene los **templates de prompts utilizados por los agentes de spec-kit** durante el flujo de **Spec-Driven Development (SDD)** del proyecto.

Los templates proporcionan **contexto del proyecto, fuentes autoritativas y disciplina arquitectónica**, pero **no redefinen el comportamiento de los agentes**.  
Su objetivo es asegurar que todos los agentes trabajen alineados con:

- la **Constitución del proyecto**
- los **ADR**
- el **roadmap**
- el **dependency graph**
- la **documentación del sistema**

Cada template corresponde a una etapa del flujo SDD.

---

# Inicialización de la Constitución

Antes de ejecutar el flujo normal de SDD debe generarse o actualizarse la **Constitución del proyecto** utilizando:

`00_constitution.md`

Este paso se utiliza para **establecer o sincronizar la Constitución con la documentación del sistema**.

Debe ejecutarse:

- **una vez al inicializar el proyecto**, o
- **cuando se modifique documentación fundamental**, como por ejemplo:
  - `docs/spec/context.md`
  - `docs/spec/roadmap.md`
  - `docs/spec/dependency-graph.yaml`
  - `docs/spec/enablers-taxonomy.md`
  - los **ADR**
  - reglas del dominio

No es necesario ejecutarlo durante el flujo habitual de desarrollo de Features o Enablers.

---

# Flujo de ejecución

El orden de ejecución recomendado es:

1. `01_specify.md`
2. `02_clarify.md` *(opcional)*
3. `03_plan.md`
4. `04_tasks.md`
5. `05_analyze.md` *(opcional)*
6. `06_implement.md`

Este orden refleja el ciclo completo desde la definición de comportamiento hasta la implementación.

---

# Descripción de cada etapa

## 00 — Constitution

Genera o actualiza la **Constitución del proyecto** a partir de la documentación existente.

Este paso establece las **reglas fundamentales y duraderas** del sistema que deben respetar todas las especificaciones, planes e implementaciones.

Se ejecuta **solo al inicio del proyecto o cuando cambian las reglas fundamentales del sistema**.

---

## 01 — Specify

Define **qué comportamiento debe tener el sistema**.

La especificación:

- describe capacidades del sistema
- define reglas de negocio
- identifica impactos arquitectónicos
- respeta la Constitución y los ADR
- **no describe implementación**

Resultado: una **spec funcional clara y reproducible**.

---

## 02 — Clarify *(opcional)*

Analiza la especificación para detectar:

- ambigüedades
- inconsistencias
- edge cases no definidos
- posibles conflictos con ADR o Constitución

Se utiliza cuando la spec necesita mayor precisión antes de planificar.

Resultado: una **spec más clara y consistente**.

---

## 03 — Plan

Define **cómo se implementará la especificación** respetando:

- arquitectura definida en ADR
- disciplina del dominio
- dependency graph
- reglas de la Constitución

El plan identifica impactos arquitectónicos y describe la estrategia general de implementación.

Resultado: un **plan de implementación alineado con la arquitectura del sistema**.

---

## 04 — Tasks

Descompone el plan en **tareas ejecutables**.

Las tareas permiten implementar la Feature o Enabler de forma incremental respetando:

- arquitectura hexagonal
- disciplina de dominio
- contratos del sistema
- dependencias del roadmap

Resultado: una **lista ordenada de tareas de implementación**.

---

## 05 — Analyze *(opcional)*

Revisa de forma global:

- la especificación
- el plan
- las tareas
- el dependency graph
- la alineación con ADR y Constitución

Se utiliza como **verificación arquitectónica antes de implementar**.

Resultado: detección temprana de inconsistencias o riesgos.

---

## 06 — Implement

Implementa el Roadmap Item siguiendo:

- la especificación
- el plan de implementación
- las tareas definidas
- los ADR del proyecto

Durante esta etapa también se debe **mantener la documentación sincronizada** con la implementación.

Resultado: implementación funcional alineada con la arquitectura y la documentación del sistema.

---

# Convención de nombres

Los templates utilizan un **prefijo numérico** para indicar el orden de ejecución:
