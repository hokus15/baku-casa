# Convenciones del sistema — Baku.Casa

Este documento define **convenciones de diseño e implementación** utilizadas en el proyecto.

Las convenciones ayudan a mantener consistencia en:

- código
- API
- persistencia
- documentación

Este documento **no define reglas invariantes del sistema**.  
Las reglas del sistema se definen en:

`docs/system/constitution.md`

---

# Convenciones de nomenclatura

## Identificadores

Los identificadores de entidades deben utilizar el formato:

```
entity_id
```

Ejemplos:

- owner_id
- property_id
- contract_id

---

## Nombres de tablas

Las tablas deben utilizar **snake_case**.

Ejemplos:

- owners
- properties
- contracts
- accruals
- payments

---

## Nombres de columnas

Las columnas deben utilizar **snake_case**.

Ejemplos:

- created_at
- updated_at
- deleted_at
- property_id

---

## Nombres de endpoints

Los endpoints deben utilizar nombres de recursos en plural.

Ejemplos:

```
/api/v1/owners
/api/v1/properties
/api/v1/contracts
```

---

# Convenciones de API

## Formato JSON

La API utiliza **JSON** como formato de intercambio.

Las claves deben utilizar **snake_case**.

Ejemplo:

```
{
  "owner_id": "123",
  "name": "Juan Pérez"
}
```

---

## Campos opcionales

Los campos con valor `null` **no deben incluirse en la respuesta de la API**.

---

## Paginación

Los endpoints de colección utilizan paginación.

Parámetros comunes:

- page
- page_size

La estructura de respuesta debe ser consistente entre endpoints.

---

# Convenciones de tiempo

Las fechas y horas deben utilizar formato **ISO 8601**.

Ejemplo:

```
2025-01-15T10:30:00Z
```

---

# Convenciones monetarias

Los importes monetarios deben representarse utilizando **Decimal**.

Ejemplo:

```
1250.50
```

Las operaciones monetarias deben evitar conversiones a tipos flotantes.

---

# Convenciones de porcentajes

Los porcentajes se representan en el rango:

```
0–100
```

Ejemplo:

```
50
```

representa **50%**.

---

# Convenciones de auditoría

Las entidades persistidas deben incluir los siguientes campos de auditoría:

- created_at
- created_by
- updated_at
- updated_by
- deleted_at
- deleted_by

---

# Convenciones de soft delete

Las entidades eliminadas mediante soft delete:

- permanecen en la base de datos
- no aparecen en consultas normales

Los endpoints de listado pueden permitir incluir registros eliminados mediante filtros explícitos.

---

# Convenciones de errores

Los errores de la API deben:

- ser estructurados
- incluir un código de error
- incluir un mensaje legible

Ejemplo:

```
{
  "error_code": "OWNER_NOT_FOUND",
  "message": "Owner not found"
}
```

---

# Convenciones de logging

Los logs deben:

- estar en inglés
- ser estructurados
- incluir correlation id cuando sea posible

---

# Convenciones de documentación

Las especificaciones deben:

- ser deterministas
- evitar ambigüedad
- describir comportamiento observable

Las especificaciones **no deben describir detalles de implementación**.

---

# Convenciones de desarrollo

El desarrollo sigue **Specification Driven Development (SDD)**.

El flujo esperado es:

1. especificación
2. planificación
3. implementación

Las implementaciones deben seguir siempre las especificaciones definidas.

# Convenciones de idioma

La documentación del proyecto utiliza dos idiomas con objetivos distintos.

## Documentación funcional

La documentación funcional debe escribirse en **español**.

Incluye:

- especificaciones de features
- especificaciones de enablers
- documentación de producto
- documentación dirigida a usuarios

Ubicación típica:

- `docs/specs/features/`
- `docs/specs/enablers/`

El objetivo es facilitar la comprensión del dominio del problema.

---

## Documentación técnica

La documentación técnica debe escribirse en **inglés**.

Incluye:

- código fuente
- comentarios en el código
- nombres de variables, funciones y tablas
- logs del sistema
- mensajes de error
- ADR (Architecture Decision Records)

El objetivo es mantener consistencia con el ecosistema técnico y facilitar colaboración técnica.