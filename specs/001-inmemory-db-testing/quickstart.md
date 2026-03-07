# Quickstart: EN-0201 Implementation Validation

## Goal
Validar que EN-0201 establece un baseline de pruebas de integración con DB en memoria para `backend/`, con esquema determinista, aislamiento entre tests y configuración de testing separada.

## 1. Preparar entorno
1. Ubicarse en `backend/`.
2. Instalar dependencias de desarrollo.
3. Confirmar disponibilidad de configuración de testing explícita y separada del runtime normal.

Comandos:

```bash
cd backend
pip install -e ".[dev]"
```

## 2. Validar activación segura del baseline
1. Ejecutar suite de integración con perfil de testing habilitado.
2. Verificar que la persistencia usada por pruebas es en memoria.
3. Confirmar que no se requieren servicios externos adicionales.
4. Ejecutar arranque normal fuera de testing y verificar que no aplica baseline de DB en memoria.

Comandos sugeridos:

```bash
pytest tests/integration/persistence/test_inmemory_activation.py
pytest tests/integration/persistence/test_no_external_dependency.py
pytest tests/integration/configuration/test_runtime_db_profile_isolation.py
```

## 3. Validar inicialización determinista de esquema
1. Ejecutar pruebas de integración en un entorno limpio.
2. Confirmar que el esquema requerido queda disponible de forma consistente antes de pruebas dependientes de persistencia.
3. Repetir ejecución y comprobar equivalencia de resultados estructurales.

## 4. Validar aislamiento entre tests
1. Ejecutar casos de integración en secuencia y luego de forma repetida.
2. Confirmar que ningún caso depende de estado producido por otro.
3. Confirmar que la política de aislamiento/limpieza evita estado residual observable entre pruebas.

## 5. Validar reproducibilidad local y CI
1. Ejecutar suite en entorno local.
2. Ejecutar la misma suite en CI.
3. Confirmar resultados consistentes bajo mismas entradas.

## 6. Quality gates
1. Ejecutar lint (`ruff`).
2. Ejecutar type-check (`mypy`).
3. Ejecutar tests (`pytest`), con foco en integración con DB en memoria y regresión contractual.

Comandos:

```bash
python -m ruff check src tests
python -m mypy src
pytest tests/integration/persistence
pytest tests/contract/auth/test_bootstrap_contract.py tests/contract/auth/test_login_logout_contract.py tests/contract/auth/test_password_change_contract.py
```
