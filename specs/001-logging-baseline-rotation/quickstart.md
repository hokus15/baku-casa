# Quickstart: EN-0200 Implementation Validation

## Goal
Validar que EN-0200 queda operativo en `backend/` con logging estructurado dual, rotacion diaria y retencion inicial de 7 dias configurable, sin cambios contractuales externos.

## 1. Preparar entorno
1. Ubicarse en `backend/`.
2. Instalar dependencias de desarrollo.
3. Verificar que existen perfiles del framework de logging en la raiz de `backend/` para `dev`, `test` y `prod` (por ejemplo `logging.dev.ini`, `logging.test.ini`, `logging.prod.ini`).

## 2. Validar carga de perfil y fallback
1. Ejecutar arranque con fichero de configuracion del framework de logging valido para entorno activo.
2. Confirmar que la aplicacion inicia y expone endpoints existentes.
3. Repetir con fichero ausente/invalido.
4. Confirmar que se aplica fallback seguro del framework manteniendo baseline minimo obligatorio de logging (sin modo "sin logging") y la aplicacion permanece operativa.
5. Confirmar contrato por entorno de escritura en consola durante fallback:
	- `dev`: salida human-friendly
	- `test`: salida human-friendly minimalista
	- `prod`: salida JSON estructurada

## 3. Validar estructura de logs y correlacion
1. Ejecutar flujos existentes de EN-0202 y F-0001 (bootstrap/login/logout/change password).
2. Confirmar emision en dos salidas: JSON y human-friendly.
3. Verificar campos obligatorios (`timestamp`, `level`, `service_name`, `correlation_id`, `message`).
4. Verificar propagacion/generacion de `correlation_id` por request.
5. Confirmar ausencia de secretos/tokens/contrasenas en registros.

## 4. Validar rotacion y retencion
1. Simular o ejecutar cruce de medianoche Europe/Madrid.
2. Confirmar creacion de nuevos ficheros tras rotacion.
3. Confirmar conservacion de logs rotados dentro de la ventana temporal configurada (valor inicial 7 dias) para JSON y human-friendly.
4. Confirmar preservacion de los ficheros activos del dia en curso.
5. Ejecutar validacion de continuidad/integridad antes y despues de la rotacion y afirmar que no se pierden eventos relevantes (mismo conjunto esperado en ambas salidas, descontando solo la segmentacion por fichero).

## 5. Validar no-regresion contractual
1. Ejecutar test suites de contrato existentes.
2. Confirmar que no hay cambios en OpenAPI ni contratos de eventos.

## 6. Quality gates
1. Ejecutar lint (`ruff`).
2. Ejecutar type-check (`mypy`).
3. Ejecutar tests (`pytest`), incluyendo integracion/contrato relevantes.

## 7. Evidencia de ejecución (2026-03-07)
1. `ruff check src tests` -> pass.
2. `C:/python/venvs/baku-casa/backend/Scripts/python.exe -m mypy src` -> pass.
3. `PYTHONPATH=src pytest -q` -> `76 passed, 4 warnings`.
4. Contratos auth (`test_bootstrap_contract.py`, `test_login_logout_contract.py`, `test_password_change_contract.py`) -> pass.
