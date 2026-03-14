# Architecture Decision Record Index — Baku.Casa

Este documento proporciona un índice de todos los **Architecture Decision Records (ADR)** del sistema.

Los ADR documentan **decisiones técnicas estructurales** que afectan al diseño del sistema.

Los ADR forman parte de las **fuentes de verdad del sistema**, tal como se define en:

`docs/system/constitution.md`

---

# ADR activos

- [ADR-0001 Monorepo Multi-root](adr/ADR-0001-monorepo-multiroot.md)
- [ADR-0002 Hexagonal Architecture](adr/ADR-0002-hexagonal-architecture.md)
- [ADR-0003 Persistence SQLite SQLAlchemy](adr/ADR-0003-persistence-sqlite-sqlalchemy.md)
- [ADR-0004 API FastAPI OpenAPI](adr/ADR-0004-api-fastapi-openapi.md)
- [ADR-0005 Authentication JWT Stateless](adr/ADR-0005-auth-jwt-stateless.md)
- [ADR-0006 Contract Versioning and Integration](adr/ADR-0006-contract-versioning-and-integration.md)
- [ADR-0007 Delivery Docker Compose Self-hosted](adr/ADR-0007-delivery-docker-compose-selfhosted.md)
- [ADR-0008 CI and Governance Model](adr/ADR-0008-ci-and-governance-model.md)
- [ADR-0009 Error Model and Observability](adr/ADR-0009-error-model-and-observability.md)
- [ADR-0010 Event Publication and Delivery](adr/ADR-0010-event-publication-and-delivery.md)
- [ADR-0011 Monetary and Percentage Representation](adr/ADR-0011-monetary-and-percentage-representation.md)
- [ADR-0012 Time Handling and Timezone Policy](adr/ADR-0012-time-handling-and-timezone-policy.md)
- [ADR-0013 Configuration System](adr/ADR-0013-configuration-system.md)
- [ADR-0014 Idempotent Operations and Duplicate Protection](adr/ADR-0014-idempotent-operations-and-duplicate-protection.md)

---

# Áreas de decisión

## Arquitectura

- ADR-0001 — Monorepo Multi-root
- ADR-0002 — Hexagonal Architecture

## Persistencia

- ADR-0003 — SQLite + SQLAlchemy

## API y contratos

- ADR-0004 — FastAPI + OpenAPI
- ADR-0006 — Contract Versioning

## Seguridad

- ADR-0005 — JWT Stateless Authentication

## Infraestructura

- ADR-0007 — Docker Compose Self-hosted

## Gobernanza

- ADR-0008 — CI and Governance Model

## Observabilidad

- ADR-0009 — Error Model and Observability

## Eventos

- ADR-0010 — Event Publication and Delivery

## Dominio financiero

- ADR-0011 — Monetary and Percentage Representation

## Tiempo

- ADR-0012 — Time Handling and Timezone Policy

## Configuración

- ADR-0013 — Configuration System

## Consistencia operativa

- ADR-0014 — Idempotent Operations and Duplicate Protection