# F-0007: Histórico de Rentas (Master Data)

## Objetivo

Gestionar el histórico de rentas efectivas de un contrato, permitiendo determinar de forma inequívoca la renta aplicable a cualquier fecha y manteniendo trazabilidad completa de las actualizaciones realizadas.

---

## Definiciones

- **Renta efectiva**: importe mensual vigente del contrato en un periodo determinado.
- **Histórico de rentas**: conjunto ordenado de entradas que representan modificaciones sucesivas de la renta.
- **Entrada de renta**: registro con rango de vigencia que define una renta efectiva.
- **Tipo de actualización**: valor perteneciente a una lista cerrada interna del sistema.
- **Renta vigente en fecha X**: entrada cuyo rango de vigencia incluye dicha fecha.
- **Renta actual**: entrada con mayor `fecha_inicio_vigencia`.

Debe existir el tipo de actualización **"Inicial"**, utilizado exclusivamente para la primera renta del contrato.

---

## Entidad

### RentHistoryEntry

**Campos obligatorios**

- `contract_id`
- `fecha_inicio_vigencia`
- `importe_final`
- `importe_inicial`
- `tipo_actualizacion`

**Campos opcionales**

- `indice_inicial`
- `indice_final`
- `tasa_variacion_indice`
- `tasa_variacion_aplicada`
- `año_inicial`
- `año_final`
- `fecha_fin_vigencia`

**Relación**

- 1 LeaseContract → 1..N RentHistoryEntry

---

## Capacidades

- Crear entrada inicial de renta al crear el contrato.
- Añadir nueva entrada de actualización.
- Editar entrada (según reglas de dominio).
- Consultar histórico completo ordenado por `fecha_inicio_vigencia`.
- Determinar renta vigente para una fecha dada.
- Obtener renta actual del contrato.

---

Las consultas de coleccion deben usar **paginacion obligatoria**.

Los parámetros de paginación configurables deben resolverse exclusivamente a través del configuration system definido en **EN-0202**.

No deben definirse mediante constantes hardcoded en adapters, servicios de aplicación o repositorios. Debe existir una única fuente de verdad para estos valores siguiendo la precedencia global de configuración:

`environment variables > config file > defaults`

## Alcance

- Persistencia completa del histórico.
- Soporte de múltiples actualizaciones sucesivas.
- Determinación determinista de renta por fecha.
- Uso de lista cerrada interna para tipos de actualización.
- Validación de coherencia temporal.
- Preparado para mapeo futuro con librería externa de índices.

---

## Fuera de alcance

- Cálculo automático del índice.
- Obtención automática de datos del índice externo.
- Generación automática de actualizaciones.
- Recalculo retroactivo masivo.
- Simulación futura de rentas.

---

## Reglas de negocio

1. Todo contrato debe tener al menos una entrada inicial de renta.
2. La primera entrada representa la renta inicial del contrato.
3. La primera entrada debe tener `tipo_actualizacion = "Inicial"`.
4. No puede existir solapamiento entre periodos de vigencia de un mismo contrato.
5. `fecha_fin_vigencia`, si existe, debe ser mayor que `fecha_inicio_vigencia`.
6. Si una nueva entrada se crea con `fecha_inicio_vigencia` posterior a otra vigente:
   - la entrada anterior debe cerrarse automáticamente estableciendo su `fecha_fin_vigencia` al día anterior.
7. La renta vigente para una fecha es la entrada cuyo rango incluye dicha fecha.
8. La renta actual es la entrada con mayor `fecha_inicio_vigencia`.
9. `importe_final` e `importe_inicial` deben ser positivos o cero.
10. `tipo_actualizacion` debe pertenecer a la lista cerrada interna del sistema.
11. La lista cerrada debe incluir obligatoriamente el tipo `"Inicial"`.
12. Las tasas y valores de índice no se recalculan automáticamente; el sistema solo los almacena.
13. `año_final` debe ser mayor o igual que `año_inicial`.
14. No puede eliminarse la única entrada de renta de un contrato activo.
15. El diseño debe permitir el mapeo futuro entre `tipo_actualizacion` interno y opciones de una librería externa.

---

---

## Dependencias y trazabilidad

### Depende de
- (ninguna explícita)

### Impacto en contratos
- HTTP API: (si aplica)
- Eventos (CloudEvents): (si aplica)

---

## ADR aplicables

### Base
- ADR-0001
- ADR-0002
- ADR-0003
- ADR-0004
- ADR-0005
- ADR-0006
- ADR-0007
- ADR-0008
- ADR-0009
- ADR-0011
- ADR-0012


---

## Baseline de observabilidad (EN-0200)

Esta feature debe alinearse con el baseline de logging transversal definido por EN-0200 cuando aplique en su implementacion:

- Campos minimos en logs: `timestamp` (UTC), `level`, `service_name`, `correlation_id`, `message`.
- Mensajes tecnicos en ingles y campos de contexto en `snake_case`.
- Exclusion de secretos, tokens y contraseñas en registros.
- Correlacion por request mediante `correlation_id`.
