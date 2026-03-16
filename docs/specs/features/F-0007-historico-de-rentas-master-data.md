# F-0007: Histórico de Rentas (Master Data)

---

## Objetivo

Gestionar el histórico de rentas efectivas de un contrato, permitiendo determinar de forma inequívoca la renta aplicable a cualquier fecha y manteniendo trazabilidad completa de las actualizaciones realizadas.

---

## Alcance

- Persistencia completa del histórico.
- Soporte de múltiples actualizaciones sucesivas.
- Determinación determinista de renta por fecha.
- Uso de lista cerrada interna para tipos de actualización.
- Validación de coherencia temporal.
- Extensibilidad para incorporar nuevos tipos de actualización en el futuro.

---

## Fuera de alcance

- Cálculo automático del índice.
- Obtención automática de datos del índice externo.
- Generación automática de actualizaciones.
- Recalculo retroactivo masivo.
- Simulación futura de rentas.

---

## Definiciones

- **Renta efectiva**: importe mensual vigente del contrato en un periodo determinado.
- **Histórico de rentas**: conjunto ordenado de entradas que representan modificaciones sucesivas de la renta.
- **Entrada de renta**: registro con rango de vigencia que define una renta efectiva.
- **Tipo de actualización**: valor perteneciente a una lista cerrada interna del sistema.
- **Renta vigente en fecha X**: entrada cuyo rango de vigencia incluye dicha fecha.
- **Renta actual**: entrada con mayor `effective_start_date`.

Debe existir el tipo de actualización **"Inicial"**, utilizado exclusivamente para la primera renta del contrato.

---

## Entidades principales

La feature introduce o utiliza las siguientes entidades del dominio:

- Renta efectiva
- Histórico de rentas

---

## Datos principales

La feature gestiona la siguiente información:

### Entidad

### RentHistoryEntry

**Campos obligatorios**

- `contract_id`
- `effective_start_date`
- `final_amount`
- `initial_amount`
- `update_type`

**Campos opcionales**

- `initial_index`
- `final_index`
- `index_variation_rate`
- `applied_variation_rate`
- `start_year`
- `end_year`
- `effective_end_date`

**Relación**

- 1 LeaseContract → 1..N RentHistoryEntry

---

## Capacidades

- Crear entrada inicial de renta al crear el contrato.
- Añadir nueva entrada de actualización.
- Editar entrada (según reglas de dominio).
- Consultar histórico completo ordenado por `effective_start_date`.
- Determinar renta vigente para una fecha dada.
- Obtener renta actual del contrato.

---

Las consultas de colección de esta feature deben seguir el contrato común definido en docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Reglas del dominio

1. Todo contrato debe tener al menos una entrada inicial de renta.
2. La primera entrada representa la renta inicial del contrato.
3. La primera entrada debe tener `update_type = "Inicial"`.
4. No puede existir solapamiento entre periodos de vigencia de un mismo contrato.
5. `effective_end_date`, si existe, debe ser mayor que `effective_start_date`.
6. Si una nueva entrada se crea con `effective_start_date` posterior a otra vigente:
   - la entrada anterior debe cerrarse automáticamente estableciendo su `effective_end_date` al día anterior.
7. La renta vigente para una fecha es la entrada cuyo rango incluye dicha fecha.
8. La renta actual es la entrada con mayor `effective_start_date`.
9. `final_amount` e `initial_amount` deben ser positivos o cero.
10. `update_type` debe pertenecer a la lista cerrada interna del sistema.
11. La lista cerrada debe incluir obligatoriamente el tipo `"Inicial"`.
12. Las tasas y valores de índice no se recalculan automáticamente; el sistema solo los almacena.
13. `end_year` debe ser mayor o igual que `start_year`.
14. No puede eliminarse la única entrada de renta de un contrato activo.
15. El modelo debe permitir incorporar nuevos tipos de actualización sin romper el histórico existente.

---

## Casos borde

La feature debe contemplar los siguientes escenarios:

- Todo contrato debe tener al menos una entrada inicial de renta.
- La primera entrada representa la renta inicial del contrato.
- La primera entrada debe tener `update_type = "Inicial"`.

---

## Dependencias

Esta feature depende de:

- F-0006

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

La lista anterior declara dependencias del item; este documento no sustituye la fuente estructural de dependencias.

---

## Shared specs aplicables

Esta feature utiliza y debe interpretarse conjuntamente con:

- docs/specs/shared/SHARED-0002-pagination-contract.md

---

## Criterios de aceptación

La feature se considera completada cuando:

- Crear entrada inicial de renta al crear el contrato.
- Añadir nueva entrada de actualización.
- Editar entrada (según reglas de dominio).

---

