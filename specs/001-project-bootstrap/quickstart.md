# Quickstart — EN-0100 Project Bootstrap

## Objetivo
Validar rápidamente que el bootstrap del proyecto está completo para avanzar a implementación detallada.

## Prerrequisitos
- Repositorio en branch `001-project-bootstrap`.
- Estructura de roots iniciales presente.
- Pipeline de CI configurado para PR.

## Verificación rápida
1. Confirmar roots iniciales `backend` y `bot`.
2. Confirmar artefactos mínimos por root: `pyproject`, `src`, `tests`.
3. Confirmar documentación base disponible (`docs/spec`, `docs/adr`, README raíz).
4. Confirmar CI en PR con checks mínimos por root:
   - lint
   - tipado
   - smoke tests
5. Confirmar exclusiones del enabler:
   - sin lógica de dominio
   - sin endpoints reales
   - sin migraciones
   - sin eventos

## Resultado esperado
- El bootstrap queda validado y listo para descomposición en tareas (`/speckit.tasks`).
- No existen impactos de contratos, persistencia ni eventos en esta fase.

## Gates de salida
- Constitution Check pre y post diseño en estado conforme.
- ADR impactados documentados con estrategia de cumplimiento.
- Artefactos de planificación (`plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`) completos.

## Regla de control de alcance (obligatoria)
- Cualquier PR de EN-0100 MUST fallar si introduce endpoints reales, migraciones, publicación de eventos o imports runtime cruzados entre `backend` y `bot`.

## Trazabilidad SDD
- `spec.md` define alcance y requisitos (FR/NFR).
- `plan.md` fija estrategia técnica y cumplimiento ADR.
- `tasks.md` descompone ejecución por fases e historias.
- `contracts/no-contract-changes.md` declara explícitamente ausencia de cambios de contrato.
