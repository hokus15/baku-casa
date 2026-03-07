# F-0002: Propietarios (Sujetos fiscales)

## Objetivo

Gestionar propietarios como entidades fiscales independientes del operador autenticado, sirviendo como “master data” para futuras asociaciones con propiedades, contratos y reporting fiscal.

---

## Definiciones

**Propietario (sujeto fiscal)**: persona o entidad titular fiscal (o potencial titular) de propiedades, usada para identificación, documentación y reporting.

- Un operador puede gestionar 0..N propietarios.
- No existen permisos por propietario (mono-usuario).

---

## Datos del propietario (mínimo viable)

### Identidad

- `owner_id`
- `tipo_persona` (lista cerrada):
  - FISICA
  - JURIDICA
- `nombre_razon_social`
- `nif` (identificador fiscal)

---

### Domicilio fiscal

- `direccion_fiscal_line1`
- `direccion_fiscal_city`
- `direccion_fiscal_postal_code`
- `direccion_fiscal_country` (default ES)

---

### Contacto (opcional)

- `email` (opcional)
- `telefono` (opcional)

---


### Metadatos

- `created_at`
- `updated_at`

---

## Capacidades

El sistema debe permitir:

- Crear propietario
- Editar propietario
- Consultar detalle de propietario
- Listar propietarios
- Buscar propietarios por `nif` y/o `nombre_razon_social`

---

## Reglas de negocio

- `nif` debe ser único por propietario.
- `tipo_persona` debe ser uno de los valores permitidos.
- No se requiere relación con propiedades en este MVP.

---

## Fuera de alcance

- Relación propietario ↔ propiedad (se introduce en Feature 1).
- Validación avanzada del formato de NIF/VAT por país.
- Multi-usuario y permisos por propietario.
- Cálculo de impuestos.

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
