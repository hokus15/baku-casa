# EN-0302 — Persistence Schema Rebaseline

## Objetivo

Consolidar el esquema de persistencia al finalizar MVP1, reemplazando el historial inicial de migraciones por un **baseline limpio del esquema de base de datos**, con el fin de simplificar la evolución futura del sistema antes de introducir el núcleo financiero (ledger).

Este enabler permite comenzar MVP2 con un modelo de persistencia estabilizado y un historial de migraciones mínimo y coherente.

---

## Descripción

Durante el desarrollo de MVP1 es habitual que el modelo de persistencia evolucione de forma iterativa mientras se explora y estabiliza el dominio (propiedades, contratos, gastos recurrentes, etc.).

Como resultado, el historial de migraciones puede contener:

- migraciones experimentales
- cambios intermedios ya obsoletos
- estructuras temporales
- inconsistencias de naming o constraints

Este enabler introduce un **punto de consolidación del esquema de persistencia** antes de iniciar el desarrollo del núcleo económico del sistema (MVP2).

El proceso consiste en:

- generar un esquema de base de datos consolidado a partir del modelo final de MVP1
- reemplazar el historial previo de migraciones por un nuevo **baseline inicial**
- asegurar que el esquema resultante es coherente, consistente y preparado para evolucionar con migraciones normales a partir de ese punto

Este proceso no introduce cambios funcionales en el dominio, sino que únicamente reorganiza la capa de persistencia.

---

## Root afectado

- `backend/`

---

## Incluye

- Consolidación del esquema de base de datos correspondiente al modelo final de MVP1.
- Generación de una nueva migración inicial que represente el estado consolidado del esquema.
- Eliminación o archivado del historial previo de migraciones generado durante el desarrollo exploratorio de MVP1.
- Verificación de que el nuevo baseline puede recrear el esquema completo de la base de datos desde cero.
- Alineación de naming, constraints e índices del esquema resultante.

---

## Fuera de alcance

- Cambios en el modelo de dominio.
- Cambios funcionales en la lógica de negocio.
- Migración o preservación de datos existentes.
- Introducción de nuevas entidades o reglas de negocio.

Este enabler asume que los datos existentes en entornos de desarrollo o testing pueden descartarse.

---

## Notas de arquitectura

Este enabler afecta exclusivamente a la capa de **Infrastructure / persistencia** y no debe introducir cambios en:

- Domain
- Application
- Interfaces

El resultado esperado es un esquema de persistencia limpio que actúe como **nuevo punto de partida para migraciones posteriores**, especialmente aquellas relacionadas con el núcleo financiero del sistema (ledger).

A partir de este punto, las migraciones deben gestionarse siguiendo el flujo normal de evolución del esquema.

---

## Criterios de aceptación

1. Existe una nueva migración inicial que representa el estado consolidado del esquema tras MVP1.
2. El esquema completo de la base de datos puede recrearse desde cero utilizando únicamente el nuevo baseline.
3. El historial previo de migraciones ha sido eliminado o archivado.
4. No se introducen cambios funcionales en el comportamiento del sistema.
5. El nuevo baseline de persistencia se utiliza como punto de partida para las migraciones de MVP2.