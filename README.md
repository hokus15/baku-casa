# Baku.Casa

Aplicación self-hosted para la gestión de alquileres de inmuebles en España.

Pensada para propietarios particulares que quieren automatizar la administración de sus propiedades y tener control claro sobre contratos, cobros y obligaciones fiscales.

---

## ¿Qué permite hacer?

### Gestión de propiedades y contratos

- Registro de propiedades
- Gestión de contratos de arrendamiento
- Control de fechas de inicio y fin
- Histórico de rentas

---

### Gestión económica

- Generación automática de devengos
- Aplicación de pagos con criterio FIFO
- Gestión de deudas y créditos
- Control de sobrepagos
- Modelado de gastos recurrentes

---

### Facturación y documentación

- Generación de recibos
- Emisión de facturas
- Representación clara de cargos y pagos aplicados

---

### Actualización de rentas

- Soporte para reglas de actualización (IPC, IRAV u otras)
- Aplicación controlada y auditable

---

### Soporte fiscal

- Preparación de información necesaria para:
  - IRPF
  - Modelo 303 (IVA)

El sistema no sustituye asesoramiento fiscal profesional.

---

### Automatización

- Generación automática de eventos internos
- Posibilidad de integración mediante webhooks o MQTT
- Automatización de tareas administrativas

---

## Características del sistema

- Funciona en red local (LAN)
- Despliegue self-hosted
- No depende de servicios externos obligatorios
- Diseñado para ejecutarse en hardware ligero (por ejemplo Raspberry Pi)
- Modelo de usuario único en el alcance inicial

---

## Enfoque

Baku está diseñado para ser:

- Determinista en sus cálculos financieros
- Auditable
- Reproducible
- Controlado por especificaciones formales

---

## Estado del proyecto

En desarrollo activo.

Las funcionalidades se implementan siguiendo un modelo de desarrollo basado en especificaciones formales y decisiones arquitectónicas documentadas.

---

## Bootstrap EN-0100

El enabler EN-0100 establece una base mínima reproducible para dos roots independientes:

- `backend`
- `bot`

Cada root incluye estructura mínima (`pyproject.toml`, `src/`, `tests/`) y un smoke test.

### Validaciones básicas locales

Backend:

1. `python -m pip install -U pytest ruff mypy`
2. `ruff check backend/src backend/tests`
3. `mypy backend/src`
4. `pytest -q backend/tests/test_smoke.py`

Bot:

1. `python -m pip install -U pytest ruff mypy`
2. `ruff check bot/src bot/tests`
3. `mypy bot/src`
4. `pytest -q bot/tests/test_smoke.py`

### Alcance EN-0100 (restricciones)

- Sin endpoints reales.
- Sin lógica de dominio.
- Sin migraciones.
- Sin publicación de eventos.
- Sin acoplamiento runtime entre roots.