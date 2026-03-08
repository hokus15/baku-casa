# Contexto del sistema

- API de gestión de alquileres de inmuebles en España.
- Maneja lógica monetaria y contable: ledger, transacciones, pagos, allocations, sobrepagos y periodificación.
- La corrección financiera, la consistencia contable y la trazabilidad histórica son críticas.
- El sistema es self-hosted y no se expone a Internet por defecto.
- El público objetivo es mayoritariamente español.
- El sistema es de larga vida y debe resistir deriva arquitectónica.

---

# Interpretación normativa

Las palabras DEBE, NO DEBE, DEBERÍA y PUEDE deben interpretarse con fuerza normativa RFC 2119.

---

# Arquitectura obligatoria

- Arquitectura hexagonal (puertos y adaptadores) como principio invariante.
- Dirección estricta de dependencias: infraestructura → aplicación → dominio.
- El dominio NO DEBE depender de frameworks, ORM, librerías de red, IO, serialización ni transporte.
- El núcleo (dominio + casos de uso) DEBE poder ejecutarse completamente en memoria.
- Está PROHIBIDO introducir entidades anémicas sin comportamiento.
- Está PROHIBIDO el uso de estado global mutable compartido.
- Está PROHIBIDO incluir lógica de negocio en controladores, modelos de persistencia o adaptadores.
- Si una regla de negocio no puede probarse sin infraestructura real, la arquitectura se considera violada.

---

# Separación estricta de modelos

- El modelo de dominio DEBE ser independiente de modelos ORM, esquemas de base de datos, DTOs de API y formatos de serialización.
- Las entidades de dominio NO DEBEN contener anotaciones de ORM ni heredar de clases de infraestructura.
- Los modelos ORM DEBEN vivir exclusivamente en infraestructura y mapear explícitamente hacia/desde el dominio.
- Los modelos de API DEBEN vivir en la capa de interfaz y NO reutilizar directamente entidades de dominio ni modelos ORM.
- El mapeo ORM ↔ Dominio y Dominio ↔ API DEBE ser explícito.
- Está PROHIBIDO exponer directamente entidades de dominio o modelos ORM como contrato externo.

---

# TDD obligatorio

- Todo cambio funcional DEBE seguir ciclo TDD: rojo → verde → refactor.
- Ningún PR puede aprobarse sin evidencia de este ciclo.

---

# Política monetaria y contable

- Está PROHIBIDO el uso de coma flotante binaria.
- Se DEBE utilizar aritmética decimal exacta.
- Redondeo obligatorio: half-up, escala 2 salvo regla explícita.
- No se permiten redondeos implícitos.
- Comparaciones monetarias DEBEN normalizar escala.
- Acumulaciones DEBEN evitar pérdida intermedia de precisión.
- Ledger inmutable.
- El ledger está compuesto exclusivamente por eventos que afectan al saldo contable/deuda:
  - Accrual (devengos) y Payment (pagos) y sus compensaciones (`reversal_of_*`).
- Otros registros con importes usados como datos estructurales o de soporte (p.ej. apuntes de adquisición/transmisión de propiedad) NO forman parte del ledger y se consideran master data económica.
- Todos los importes monetarios persistidos DEBEN ser no negativos (>= 0).
- Está PROHIBIDO cualquier forma de borrado lógico o flag de cancelación en eventos del ledger.
- No se permite `deleted_at`, flags de cancelación ni modificaciones en eventos del ledger.
- Los eventos económicos (Accrual, Payment, Invoice emitida y sus rectificativas) son estrictamente append-only.
- Las correcciones se realizan exclusivamente mediante eventos compensatorios (`reversal_of_*`).
- En entidades NO económicas (master data, configuración, contratos, cláusulas, plantillas, tareas, etc.) se PERMITE borrado lógico (soft delete).
- El borrado lógico en entidades no económicas DEBE ser explícito y auditable (`deleted_at`, `deleted_by`).
- Correcciones exclusivamente mediante asientos de compensación.
- La compensación es siempre TOTAL en eventos económicos del ledger (Accrual, Payment).
- En documentos fiscales (Invoice) se permite compensación TOTAL o PARCIAL mediante facturas rectificativas, sin alterar el saldo contable (que se calcula solo desde Accrual y Payment).
- Ajustes de redondeo deben ser explícitos y trazables.
- Los eventos económicos del ledger (Accrual y Payment) DEBEN ser inmutables (append-only).
- Los documentos fiscales (Invoice emitida y sus rectificativas) son inmutables, pero no forman parte del ledger contable.
- Todo evento compensatorio DEBE referenciar el original mediante `reversal_of_*`.
- El efecto económico (signo) NO se persiste: se deriva como + para eventos normales y - para eventos compensatorios.
- Todo caso de uso que cree eventos económicos DEBE requerir `idempotency_key` obligatorio.
- Conservación exacta de valor (suma algebraica = 0 considerando signos derivados).
- Allocations deben cuadrar exactamente.
- Las operaciones económicas DEBEN ser idempotentes y no duplicar efectos ante repetición.

---

# Representación de porcentajes

- Los porcentajes DEBEN representarse en el rango 0–100 en todas las capas del sistema.
- Está PROHIBIDO utilizar representaciones fraccionarias 0–1 como modelo persistente o de dominio.
- Los porcentajes DEBEN modelarse como tipo de dominio explícito.
- Las conversiones a fracción SOLO pueden realizarse localmente para cálculo y NO forman parte del contrato.

---

# Modelo temporal y contratos de fecha

- Zona horaria interna obligatoria: UTC.
- Conversiones solo en bordes.
- Fechas y timestamps DEBEN representarse en ISO-8601.
- No se permiten strings libres de fecha como contrato.
- Fecha de devengo y fecha de registro DEBEN diferenciarse.
- Reportes contables DEBEN basarse en fecha de devengo.

---

# Concurrencia e idempotencia

- Las operaciones económicas DEBEN proteger invariantes frente a concurrencia.
- Los agregados contables DEBEN protegerse mediante control de concurrencia explícito (optimista o equivalente).
- No se permite “last write wins” en entidades contables.
- El sistema DEBE permitir identificar solicitudes repetidas sin duplicar efectos.
- Las operaciones económicas DEBEN ser idempotentes y no duplicar efectos ante repetición.
- Las operaciones económicas DEBEN ejecutarse dentro de una transacción atómica (commit/rollback) que preserve invariantes.
- La idempotencia DEBE implementarse mediante un identificador de idempotencia persistido con unicidad a nivel de almacenamiento.
- Ante conflicto de concurrencia, el sistema DEBE fallar de forma explícita (sin reintentos silenciosos no acotados) y devolver un error tipificado de conflicto.

---

# Identidades e IDs opacos

- Toda entidad persistente DEBE usar ID opaco interno.
- El ID NO DEBE codificar información semántica.
- Debe ser globalmente único e inmutable.
- No se reutiliza ni reasigna.
- Validación por formato/longitud, nunca por significado.
- IDs externos deben almacenarse separados y mapearse explícitamente.

---

# Enumeraciones

- Todo conjunto cerrado DEBE modelarse como enumeración.
- Se prohíben literales repetidos.
- Enumeraciones DEBEN definirse una sola vez (DRY).
- Si procede maestro-detalle real, NO debe degradarse a enumeración.

---

# Diseño de API y contratos

- La API DEBE ser orientada a recursos.
- Las operaciones DEBEN mapearse semánticamente a métodos HTTP estándar.
- Todo endpoint de colección DEBE estar paginado mediante parámetros consistentes y una estructura de respuesta uniforme.
- Está PROHIBIDO devolver listas no acotadas.
- El contrato de paginación DEBE ser consistente.
- Filtros y ordenación DEBEN ser explícitos.
- Las estructuras de respuesta NO DEBEN depender de modelos ORM.
- Los DTOs públicos DEBEN ser explícitos y estables.
- Los campos cuyo valor sea `null` NO DEBEN incluirse en las respuestas de la API pública, salvo que el contrato del endpoint requiera explícitamente su presencia.
- La ausencia de un campo en la respuesta DEBE interpretarse como ausencia de valor (`null` o no aplicable) salvo que la documentación del endpoint indique lo contrario.
- Cambios incompatibles requieren versionado mayor.
- La versión MAYOR del contrato HTTP DEBE expresarse en la ruta base (p. ej. `/api/v1`).
- Dentro de una misma versión MAYOR, los cambios DEBEN ser retrocompatibles (solo añadir campos opcionales; no renombrar/eliminar; no cambiar significado).
- La especificación OpenAPI DEBE publicarse para cada versión MAYOR y representar el contrato real (source of truth).
- La eliminación de campos/endpoints solo se permite al incrementar versión MAYOR y DEBE quedar documentada.

---

# Errores y contratos

- Los errores DEBEN estar tipificados.
- Cada error DEBE tener código estable en inglés.
- El mensaje descriptivo DEBE estar en español.
- No se permite capturar excepciones genéricas y ocultar contexto.
- Los errores DEBEN mapearse a códigos HTTP semánticos y consistentes (p. ej. validación 400, auth 401/403, no encontrado 404, conflicto de concurrencia 409).
- La respuesta de error DEBE incluir un identificador de correlación/traza para diagnóstico.

---

# Auditoría estructural

- Toda entidad persistente modificable DEBE ser auditable.
- Debe registrarse created_at, created_by, updated_at, updated_by.
- El ledger y los eventos económicos NO permiten modificación ni borrado.
- En entidades no económicas, si se utiliza borrado lógico:
  - DEBE registrarse `deleted_at` y `deleted_by`.
  - El borrado lógico NO puede romper integridad referencial histórica.
- La auditoría NO DEBE depender exclusivamente de mecanismos implícitos del ORM.
- Los eventos económicos DEBEN ser append-only: no se permite deleted_at en eventos económicos; solo compensaciones.

---

# Observabilidad

- Logs técnicos en inglés.
- Correlation ID obligatorio.
- Logging estructurado con contexto suficiente.
- Cada registro de log DEBE incluir al menos: timestamp (UTC), level, service name, correlation_id, message.
- Rotación de ficheros de log diaria a medianoche (Europe/Madrid).
- Logs NO deben incluir PII por defecto.

## Excepción explícita de configuración para logging framework (EN-0200)

- Como excepción acotada, los perfiles de configuración del framework de logging PUEDEN
  definirse como artefactos operativos externos en la raíz de `backend/` (por ejemplo,
  `logging.dev.ini`, `logging.test.ini`, `logging.prod.ini`).
- Esta excepción aplica solo a configuración específica del framework de logging y NO
  puede extenderse a otros dominios de configuración runtime.
- La aplicación PUEDE cargar directamente el perfil activo del framework de logging en
  arranque.
- Si el perfil falta o es inválido, la aplicación PUEDE aplicar fallback seguro del
  framework, pero SIEMPRE manteniendo baseline mínimo obligatorio de logging
  (timestamp UTC, level, service name, correlation_id, message); no se permite
  operación efectiva sin logging.
- Contrato de fallback por entorno (escritura en consola):
  - `dev`: salida human-friendly.
  - `test`: salida human-friendly minimalista.
  - `prod`: salida JSON estructurada.
- Esta excepción DEBE mantenerse alineada con ADR-0009 (observabilidad) y ADR-0013
  (configuration system).

---

# Principios de Ingeniería

- Se debe aplicar el principio DRY (Do Not Repeat Yourself) cuando la duplicación represente conocimiento de negocio compartido dentro del mismo contexto arquitectónico.
- La duplicación intencionada puede ser aceptable cuando sea necesaria para preservar límites arquitectónicos estrictos (por ejemplo, entre roots independientes del monorepo).
- Ningún principio de reutilización debe violar las fronteras definidas por la arquitectura hexagonal ni el aislamiento entre componentes.
- La reducción de duplicación nunca debe comprometer la claridad, la independencia de módulos o la integridad de los contratos versionados.

---

# Multi-root

- `backend/`, `frontend/` y `bot/` son independientes.
- Cada root con su propio pyproject.toml.
- No se permite código compartido de runtime.
- Integración solo mediante contratos versionados.
- Tests de contrato obligatorios.

---

# Entrega y contenedores

- Cada root se entrega como imagen independiente.
- Imágenes reproducibles y mínimas.
- Configuración en runtime.
- Secretos nunca en imagen.
- Ejecutar como usuario no-root salvo justificación.
- Manejo correcto de SIGTERM.
- Healthchecks obligatorios.

---

# Orquestación y perfiles

- Orquestación tipo Compose obligatoria.
- Servicios sobre red privada interna.
- No exponer puertos salvo necesidad explícita.
- Perfiles dev/prod con base común.
- prod debe minimizar exposición.

---

# Exposición API

- Accesible desde localhost o LAN.
- No exponer a Internet por defecto.
- Exposición pública solo mediante decisión explícita y protección adicional.

---

# Política de backups y recuperación

- El sistema DEBE permitir realizar copias de seguridad completas del estado persistente.
- La restauración DEBE ser verificable y preservar la integridad contable.
- Las migraciones de esquema DEBEN ser reproducibles y no comprometer la restaurabilidad.
- Cada release DEBE incluir el conjunto completo de migraciones necesarias para actualizar desde el esquema soportado más antiguo.
- Debe existir al menos una prueba automatizada de upgrade que verifique: backup → migración → restore → checks de integridad contable.
- No se permiten migraciones destructivas sin estrategia explícita de preservación/transformación de datos y verificación posterior.

---

# Política de idioma

- Documentación funcional en español.
- Código y logs técnicos en inglés.
- Contratos públicos en inglés.
- No mezclar idiomas en código.

---

# Flujo de desarrollo y quality gates

- Cada feature inicia con spec aprobada.
- Plan técnico debe incluir Constitution Check.
- PR debe validar lint, tipado y tests.
- Incumplimientos deben registrarse con plan de eliminación.

---

# Governance

- Esta constitución prevalece sobre cualquier guía operativa.
- Enmiendas requieren propuesta documentada y estrategia de migración.
- Versionado: MAJOR / MINOR / PATCH.