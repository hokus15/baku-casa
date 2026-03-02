/speckit.plan Feature <N>

Genera el plan de implementación para esta Feature.

Fuentes autoritativas:
- docs/spec/context.md
- docs/spec/roadmap.md
- docs/spec/features/<nombre-fichero-feature>.md
- docs/adr/ADR-0001..ADR-0012

El plan debe cumplir estrictamente todos los ADR aceptados.

---

## Disciplina Arquitectónica Obligatoria

El plan DEBE:

1. Identificar explícitamente los ADR materialmente impactados.
2. Explicar cómo la implementación cumplirá cada ADR impactado.
3. Declarar si hay cambios de contrato (HTTP o eventos).
4. Declarar si hay cambios de persistencia (migraciones).
5. Declarar si introduce eventos (y aplicar ADR-0010).
6. Declarar si requiere el profile `events` en docker-compose.
7. Declarar implicaciones de versionado.

Si la Feature requiere modificar o crear un nuevo ADR, debe indicarse como "ADR Gap".

---

## Restricciones Técnicas

El plan debe respetar:

- Arquitectura hexagonal (sin lógica de negocio en adapters).
- Persistencia SQLite con transacciones explícitas.
- Dinero y porcentajes como Decimal (0–100).
- Tiempos en UTC.
- JWT stateless con credential_version.
- CloudEvents para eventos.
- Outbox obligatorio si hay eventos.
- Paginación obligatoria para endpoints de lista.
- Error model tipificado.
- Contract tests obligatorios si se modifican contratos.

---

## Exclusiones

No incluir código.
No generar migraciones concretas.
No describir tests en detalle (solo estrategia).
No repetir la spec funcional.

---
