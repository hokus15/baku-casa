# Glosario del sistema — Baku.Casa

Este documento define los **términos fundamentales del sistema**.

Su objetivo es evitar ambigüedad y garantizar que los mismos conceptos se utilicen de forma consistente en:

- especificaciones
- ADR
- documentación técnica
- implementación

Este documento **no define reglas** ni comportamiento del sistema.

Las reglas del sistema se definen exclusivamente en:

`docs/system/constitution.md`

---

# Operador

Persona que utiliza el sistema para gestionar propiedades y contratos.

Características:

- existe un único operador en el sistema
- el operador administra toda la información
- el operador no representa necesariamente a un propietario

---

# Propietario

Entidad fiscal que posee total o parcialmente una propiedad.

Puede ser:

- persona física
- persona jurídica

Un propietario **no es un usuario del sistema**.

Es una entidad utilizada para modelar titularidad fiscal.

---

# Sujeto fiscal

Entidad que puede ser titular fiscal de una propiedad.

En el contexto del sistema, normalmente coincide con el **propietario**.

---

# Propiedad

Unidad inmobiliaria gestionada por el sistema.

Ejemplos:

- vivienda
- apartamento
- local comercial
- plaza de aparcamiento
- trastero

Una propiedad puede tener **uno o varios propietarios**.

---

# Titularidad

Relación entre un propietario y una propiedad.

Define:

- qué propietario es titular
- qué porcentaje de la propiedad posee

---

# Contrato de alquiler

Acuerdo entre un propietario y un inquilino para el uso de una propiedad.

Define:

- fecha de inicio
- fecha de fin
- renta
- condiciones de pago

---

# Inquilino

Persona o entidad que alquila una propiedad.

El inquilino **no es un usuario del sistema**.

Es una entidad utilizada para modelar relaciones contractuales.

---

# Evento económico

Registro que representa una operación económica en el sistema.

Los eventos económicos forman parte del **ledger del sistema**.

Eventos permitidos:

- Accrual
- Payment

---

# Ledger

Registro cronológico de todos los eventos económicos del sistema.

Características:

- append-only
- los eventos históricos no se modifican
- las correcciones se realizan mediante reversiones

---

# Accrual (devengo)

Evento económico que representa la generación de una obligación económica.

Ejemplo típico:

- devengo de una renta mensual de alquiler

Un accrual representa **una cantidad que debe pagarse**.

---

# Payment (pago)

Evento económico que representa la recepción de un pago.

Un payment puede compensar total o parcialmente uno o varios accruals.

---

# Compensación

Proceso mediante el cual un pago se aplica a uno o varios accruals.

El objetivo es reducir o eliminar la deuda pendiente.

---

# Reversión

Evento que corrige un evento económico anterior.

Las correcciones **no modifican el evento original**.

En su lugar se crea un nuevo evento que lo revierte.

---

# Deuda

Cantidad pendiente derivada de accruals que todavía no han sido compensados por pagos.

---

# Sobrepago

Situación en la que el total de pagos supera el total de accruals pendientes.

---

# DTO

Objeto utilizado para transportar datos entre el backend y el exterior del sistema.

Los DTOs forman parte de los **contratos de API**.

Los DTOs **no deben exponer entidades ORM**.

---

# ORM

Modelo utilizado para representar datos persistidos en la base de datos.

Los modelos ORM **no deben utilizarse como contratos de API**.

---

# Feature

Capacidad funcional del sistema.

Una feature describe comportamiento visible del sistema.

Las features se definen en:

`docs/specs/features/`

---

# Enabler

Capacidad técnica que habilita funcionalidades del sistema.

Los enablers suelen introducir:

- infraestructura
- capacidades transversales
- mejoras arquitectónicas

Los enablers se definen en:

`docs/specs/enablers/`

---

# Baseline técnico

Conjunto de capacidades técnicas introducidas por enablers que deben asumirse como disponibles por futuras features.

El baseline técnico se define mediante el dependency graph.

---

# Dependency graph

Documento que define:

- dependencias entre features y enablers
- orden de implementación
- propagación del baseline técnico

Ubicación:

`docs/planning/dependency-graph.yaml`

---

# Soft delete

Técnica de eliminación lógica de registros.

Un registro marcado como eliminado:

- permanece en la base de datos
- no aparece en consultas normales

---

# Auditoría

Registro de información sobre la creación y modificación de entidades.

Campos típicos:

- created_at
- created_by
- updated_at
- updated_by
- deleted_at
- deleted_by