# Convenciones del sistema — Baku.Casa

Este documento define **convenciones de expresión, nomenclatura y estilo** utilizadas en el proyecto.

Las convenciones ayudan a mantener consistencia en:

- código
- contratos externos
- persistencia
- documentación

Este documento **no define reglas invariantes del sistema** ni decisiones tecnológicas concretas.  
Las reglas globales se definen en:

`docs/system/constitution.md`

Las decisiones técnicas concretas se documentan en:

`docs/decisions/adr/`

Si una convención pasa a ser un requisito obligatorio del sistema, **DEBE promocionarse** a la constitución, a un ADR o a una shared spec, según corresponda.

---

# Convenciones de nomenclatura

## Identificadores

Los identificadores de entidades deben utilizar el formato:

```text
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

Los endpoints deben utilizar nombres de recursos en plural cuando el contrato exponga colecciones.

Ejemplos:

```text
/api/v1/owners
/api/v1/properties
/api/v1/contracts
```

---

# Convenciones de API

## Formato JSON

La API utiliza **JSON** como formato de intercambio cuando el contrato sea JSON.

Las claves deben utilizar **snake_case**.

Ejemplo:

```json
{
  "owner_id": "123",
  "name": "Juan Pérez"
}
```

---

## Representación temporal en interfaces

Las fechas y horas expuestas en interfaces textuales deben utilizar formato **ISO 8601** cuando el contrato no establezca un formato más específico.

Ejemplo:

```text
2025-01-15T10:30:00Z
```

---

# Convenciones de documentación

## Redacción de especificaciones

Las especificaciones deben:

- describir comportamiento observable
- usar terminología consistente con el glosario
- evitar redacción ambigua

Las especificaciones no deben introducir detalles de implementación salvo referencia explícita a un ADR o a una nota auxiliar claramente marcada como no normativa.

---

## Referencias cruzadas

Cuando una spec dependa de una regla global, una decisión técnica o un catálogo compartido, debe **referenciar la fuente autoritativa** en lugar de reescribirla.

---

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
