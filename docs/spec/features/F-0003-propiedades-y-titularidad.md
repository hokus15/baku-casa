# F-0003: Propiedades y Titularidad

## Objetivo

Permitir registrar propiedades y vincularlas a uno o varios propietarios (sujetos fiscales), estableciendo la titularidad actual sin histórico.

Este slice habilita la base estructural para contratos, contabilidad y fiscalidad.

---

## Definiciones

**Propiedad**: unidad inmobiliaria gestionable.

**Titularidad**: relación entre Propiedad y Propietario con porcentaje de participación.

- Una propiedad tiene 1..N propietarios.
- Un propietario puede tener 0..N propiedades.
- No se guarda histórico de cambios de titularidad (solo estado actual).

---

## Datos de la propiedad

- `property_id`
- `nombre`
- `tipo` (lista cerrada):
  - Vivienda
  - Apartamento
  - Plaza de aparcamiento
  - Estudio
  - Local comercial
  - Oficina
  - Trastero
  - Otro
- `descripción` (opcional)
- `dirección` (opcional)
- `ciudad` (opcional)
- `codigo postal` (opcional)
- `provincia` (opcional)
- `pais` (opcional)
- `referencia_catastral` (opcional)
- `valor_catastral` (opcional)
- `valor_catastral_suelo` (opcional)
- `valor_catastral_construccion` (calculado = valor_catastral − valor_catastral_suelo) (opcional)
- `proporcion_construccion` (calculado = valor_catastral_construccion / valor_catastral) (opcional)
- `valor_catastral_revisado` (boolean) (opcional)
- `fecha de adquisición` (opcional)
- `tipo de adquisición` (opcional) (lista cerrada) Tipo de adquisición para el informe de IRPF:
  - Onerosa
  - Lucrativa
  - Ambas
- `fecha de transmision` (opcional)
- `tipo de transmision` (opcional) (lista cerrada) Tipo de transmision para el informe de IRPF:
  - Onerosa
  - Lucrativa
  - Ambas
- `naturaleza fiscal` (opcional) (lista cerrada):
  - Urbana
  - Rústica
- `situacion fical` (opcional) (lista cerrada):
  - Con referencia catastral
  - Situado en el Pais Vasco
  - Situado en Navarra
  - Sin referencia catastral
---

## Titularidad

La relación Propiedad ↔ Propietario incluye:

- `owner_id`
- `property_id`
- `porcentaje_participacion`

---

## Capacidades

El sistema debe permitir:

- Crear propiedad
- Editar propiedad
- Consultar detalle de propiedad
- Listar propiedades
- Asignar propietarios a una propiedad
- Modificar porcentajes de titularidad
- Consultar propiedades de un propietario
- Consultar propietarios de una propiedad

---

## Reglas de negocio

- Una propiedad debe tener al menos un propietario.
- `tipo` debe ser uno de los valores permitidos.
- `valor_catastral_construccion` y `proporcion_construccion` son campos derivados y no editables directamente.

---

## Fuera de alcance (en este slice)

- Operación de adquisición y venta.
- Gastos recurrentes.
- Amortizaciones fiscales.
- Contratos.
- Contabilidad.
- Facturación.

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
