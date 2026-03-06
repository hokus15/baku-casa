# EN-0201: In-Memory Database Testing Baseline

## Objetivo
Establecer un baseline de testing que permita ejecutar tests de integración con base de datos **en memoria** de forma rápida, reproducible y aislada, garantizando:

- inicialización determinista del esquema
- aislamiento entre tests
- configuración de testing separada del runtime normal
- ejecución sin dependencias externas

---

## Descripción
El sistema requiere tests que verifiquen integración real con persistencia (transacciones, repositorios, consultas) sin introducir dependencias externas ni complejidad operativa. Una base de datos en memoria permite ejecutar tests de forma rápida y repetible, manteniendo el ciclo de feedback corto.

Este enabler define los requisitos mínimos para que los tests puedan levantar una base de datos en memoria, crear el esquema, ejecutar casos de prueba y limpiar el estado entre ejecuciones, sin afectar a la configuración de producción/desarrollo.

---

## Root afectado
- `backend/`

---

## Incluye
- Definición de una configuración de testing específica que habilite el uso de base de datos en memoria.
- Inicialización determinista del esquema para tests:
  - creación del schema al inicio de ejecución de tests (o por suite)
  - mecanismo equivalente para garantizar que el schema coincide con el modelo persistente
- Aislamiento entre tests:
  - cada test no debe depender de estado persistente generado por otro test
  - estrategia consistente para limpieza/rollback/recreación del estado
- Ejecución de tests sin dependencias externas (sin servicios adicionales).
- Convenciones para:
  - naming y ubicación de tests que requieren DB
  - marcadores o categorías para distinguir tests unitarios vs integración con DB (si aplica)
- Garantía de que el enfoque es compatible con ejecución en CI y entornos locales.

---

## Fuera de alcance
- Performance benchmarking.
- Tests end-to-end que dependan de servicios externos.
- Selección de framework de testing o runner específico (la suite puede evolucionar).
- Herramientas de migraciones específicas (solo se requiere que el esquema sea determinista para tests).

---

## Notas de arquitectura
- La base de datos en memoria se utiliza exclusivamente para tests y no debe afectar a la configuración de runtime normal.
- Los tests con DB deben validar interacciones de persistencia reales sin filtrar lógica de negocio hacia adaptadores.
- La configuración de testing debe poder activarse de manera explícita y segura (sin riesgo de ejecutar contra entornos persistentes por error).
- El diseño debe permitir mantener el modelo de dominio desacoplado de detalles ORM.

---

## Criterios de aceptación
1. Los tests de integración pueden ejecutarse utilizando una base de datos en memoria sin dependencias externas.
2. El esquema de base de datos para tests se inicializa de forma determinista y consistente.
3. Los tests con DB son aislados: no existe dependencia de estado entre tests.
4. Existe una configuración de testing separada y no ambigua para habilitar DB en memoria.
5. La ejecución local y en CI produce resultados consistentes.