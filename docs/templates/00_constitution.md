# Spec-Kit Prompt Template — `/speckit.constitution`

Genera la Constitución del proyecto a partir de la documentación existente, tomando como fuente principal la Constitución actual y manteniendo coherencia con el resto de documentos autoritativos.

---

# Fuentes Autoritativas

Debes basarte exclusivamente en:

- `docs/spec/constitution.md`
- `docs/spec/context.md`
- `docs/spec/roadmap.md`
- `docs/spec/dependency-graph.yaml`
- `docs/spec/enablers-taxonomy.md`
- `docs/spec/features/`
- `docs/spec/enablers/`
- `docs/adr/ADR-0001..ADR-0014`

La Constitución no puede contradecir ninguno de estos documentos.

La fuente principal es:

- `docs/spec/constitution.md`

En caso de conflicto, debes señalarlo explícitamente en lugar de resolverlo de forma implícita.

---

# Rol de la Constitución

La Constitución debe recoger las reglas fundamentales y duraderas del proyecto.

Debe servir como referencia común para:

- especificaciones
- clarificaciones
- planes
- tareas
- implementaciones

Debe contener principios y reglas estables del sistema, no decisiones accidentales ni detalles efímeros.

---

# Disciplina de ADR

La Constitución debe ser coherente con todos los ADR vigentes.

No debe contradecir ADR existentes.

No debe redefinir innecesariamente decisiones ya formalizadas en ADR.

Si detectas que alguna regla relevante no está suficientemente cubierta por los ADR actuales, debes indicarlo en:

```
ADR Gap
```

---

# Consistencia con el Dominio

La Constitución debe preservar las reglas fundamentales del dominio del sistema.

Especialmente en aspectos como:

- representación de dinero
- representación de porcentajes
- disciplina temporal
- modelo de errores
- reglas del dominio económico y contable

---

# Consistencia con el Roadmap

La Constitución debe ser compatible con:

- la estructura del roadmap
- el dependency graph
- la separación entre Features y Enablers

No debe introducir restricciones que rompan la evolución prevista del sistema.

---

# Consistencia de Documentación

Debes comprobar la alineación entre:

- la Constitución actual
- el roadmap
- el dependency graph
- los ADR
- la documentación funcional y habilitadora

Si detectas inconsistencias o vacíos normativos debes señalarlos explícitamente.

Debes priorizar la preservación de la intención normativa ya existente en `docs/spec/constitution.md`, refinándola y corrigiendo inconsistencias solo cuando sea necesario para mantener coherencia con el resto de documentación autoritativa.

---

# Restricciones

La Constitución NO debe:

- describir implementación concreta
- introducir frameworks o tecnologías específicas
- definir estructura de código
- duplicar innecesariamente contenido de ADR
- incluir reglas inestables o demasiado cambiantes

Debe centrarse en principios, restricciones y reglas duraderas del proyecto.