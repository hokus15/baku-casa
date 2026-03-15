# Objetivo

Generar un nuevo **Architecture Decision Record (ADR)** para el proyecto Baku.Casa a partir de un texto fuente.

El texto fuente puede describir:

- una decisión técnica ya tomada
- una alternativa evaluada
- una restricción técnica relevante
- un cambio arquitectónico que necesita quedar documentado

El resultado debe seguir la estructura definida en:

docs/decisions/templates/adr-template.md

---

# Contexto

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
docs/system/conventions.md  
docs/decisions/ADR-INDEX.md  
docs/decisions/templates/adr-template.md  
docs/meta/doc-governance.md  
docs/README.md

---

# Idioma

El ADR generado debe escribirse **en inglés**, siguiendo el estilo de los ADR ya existentes del proyecto.

Las instrucciones de este prompt están en castellano, pero la salida final debe quedar alineada con:

docs/decisions/adr/

---

# Entrada esperada

Se proporcionará un **texto fuente** con la decisión o el problema a documentar.

Ese texto puede ser:

- breve o extenso
- más narrativo o más técnico
- una decisión ya resuelta o una propuesta suficientemente madura

---

# Instrucciones

1. Determinar si el texto fuente describe realmente una **decisión técnica o arquitectónica**.

2. Si el texto describe una **regla global e independiente del stack**, no convertirla en ADR:

- debe tratarse como materia de `docs/system/constitution.md`

3. Si el texto describe **comportamiento funcional de dominio**, no convertirlo en ADR:

- debe tratarse como spec de feature o enabler

4. Si el texto sí corresponde a una decisión técnica o arquitectónica:

- generar el ADR usando:

docs/decisions/templates/adr-template.md

5. Rellenar todos los placeholders:

{{FIELD_NAME}}

6. Eliminar todos los bloques de instrucción:

<<INSTRUCTION>>
...
<<END_INSTRUCTION>>

El documento final **NO debe contener placeholders ni bloques de instrucción**.

---

# Reglas

El ADR generado:

- DEBE documentar una **decisión técnica concreta**
- DEBE explicar claramente el **contexto que obliga a decidir**
- DEBE dejar explícita la **decisión adoptada**
- DEBE reflejar **alternativas consideradas**
- DEBE describir **consecuencias y trade-offs**
- DEBE poder actuar como fuente autoritativa para planes e implementaciones futuras

El ADR generado:

- NO DEBE redefinir reglas globales que pertenezcan a `docs/system/constitution.md`
- NO DEBE describir comportamiento funcional que pertenezca a una spec
- NO DEBE convertirse en una guía de implementación paso a paso
- NO DEBE duplicar ADRs existentes si la decisión ya está documentada

Si el texto fuente entra en conflicto con un ADR vigente, debe prevalecer la coherencia con la documentación autoritativa existente salvo que el nuevo ADR sustituya explícitamente al anterior.

---

# Uso de fuentes autoritativas

Antes de redactar el ADR, contrastar el texto fuente con:

- `docs/system/constitution.md`
- `docs/system/context.md`
- `docs/decisions/ADR-INDEX.md`

Objetivos:

- evitar que una regla constitucional se documente erróneamente como ADR
- evitar duplicar una decisión ya existente
- mantener coherencia con restricciones operativas ya documentadas

Si el nuevo ADR depende claramente de otro ADR, debe referenciarlo en `Context` o `Decision` cuando sea material.

---

# Status

Elegir el `Status` más adecuado según la madurez del texto fuente:

- `Proposed` si la decisión todavía no está consolidada
- `Accepted` si la decisión ya está asumida por el proyecto
- `Superseded` si este ADR documenta una decisión reemplazada
- `Deprecated` si la decisión sigue existiendo como referencia histórica pero ya no debe guiar el sistema

No inventar un estado distinto salvo que el repositorio lo adopte explícitamente.

---

# Context

La sección `Context` debe incluir:

- el problema o necesidad técnica
- restricciones relevantes
- drivers de decisión
- dependencias con otras decisiones si existen

No debe incluir todavía la solución.

---

# Decision

La sección `Decision` debe:

- expresar la decisión de forma normativa y clara
- dejar visibles las reglas vinculantes derivadas
- usar lenguaje consistente con los ADR existentes (`SHALL`, `MUST`, `MUST NOT`, `MAY`, `SHOULD`) cuando ayude a fijar la decisión

Si la decisión requiere subsecciones internas, deben mantenerse claras y escaneables.

---

# Alternatives Considered

Deben describirse solo alternativas plausibles y realmente comparables.

Cada alternativa debe indicar claramente por qué no fue elegida.

No inventar alternativas absurdas o irrelevantes solo para rellenar la estructura.

---

# Consequences

La sección `Consequences` debe separar al menos:

- efectos positivos
- trade-offs o costes
- impacto operativo, si aplica
- mecanismos de verificación

Las consecuencias deben ser específicas y útiles para futuras fases de `plan` e `implement`.

---

# Plan Enforcement

La sección `Plan Enforcement` debe traducir la decisión en reglas accionables para futuros planes e implementaciones.

Debe dejar claro qué incumplimientos invalidarían un plan afectado por este ADR.

---

# Salida esperada

Devolver **únicamente el documento Markdown final** del ADR.

No incluir explicaciones, comentarios ni análisis fuera del propio ADR.

El resultado debe poder guardarse directamente como:

docs/decisions/adr/ADR-XXXX-nombre.md
