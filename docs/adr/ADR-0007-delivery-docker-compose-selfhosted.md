# ADR-0007: Delivery Model (Docker Compose, Self-Hosted, Profile-Based Services)

## Status
Accepted

## Context

The system is designed to be self-hosted on lightweight hardware (e.g., Raspberry Pi).

Key constraints:

- No external managed infrastructure.
- Minimal operational complexity.
- Deterministic and reproducible deployment.
- Optional event-driven integration (see ADR-0006).
- No unnecessary exposed services.
- Security-first local deployment model.

A consistent and enforceable delivery model is required to guarantee reproducibility and isolation.


## Decision

The system SHALL use **Docker and Docker Compose** as the exclusive deployment mechanism.

All runtime components MUST be containerized.

---

## Containerization Rules

- Each root (`backend/`, `bot/`, future roots) MUST produce its own Docker image.
- Images MUST be built independently.
- Containers MUST run as non-root users.
- Containers MUST handle SIGTERM gracefully.
- Images MUST be reproducible from source using deterministic builds.

---

## Docker Compose as Orchestrator

- Docker Compose is the mandatory orchestration mechanism.
- The repository root MUST contain a `docker/` directory.
- The `docker-compose.yml` file MUST define all services.
- Environment configuration MUST be externalized (no secrets in images).

---

## Profile-Based Optional Services

Docker Compose profiles MUST be used to enable optional components.

### Mandatory Profile

The default profile MUST include:

- backend
- bot (if enabled by feature scope)

### Optional Profiles

An `events` profile MAY include:

- MQTT broker

When the `events` profile is disabled:

- The system MUST remain fully functional.
- No core feature may depend on MQTT unless explicitly declared in its plan (see ADR-0006).

---

## Network Exposure Policy

- Services MUST bind to internal Docker networks by default.
- Ports MUST NOT be exposed to the public internet by default.
- Exposure beyond localhost/LAN requires explicit configuration.
- The system assumes a LAN-only deployment model.

---

## Persistence and Volumes

- SQLite database files MUST be mounted using Docker volumes.
- Volumes MUST ensure data durability across container restarts.
- Backup procedures MUST operate on mounted volumes (see ADR-0003).

---

## Infrastructure Constraints

- No external managed services (database, Redis, managed MQTT).
- All optional infrastructure MUST be local and self-contained.
- MQTT broker, if enabled, MUST run inside Docker Compose.

---

## Security Requirements

- Secrets MUST be injected via environment variables or Docker secrets.
- No hard-coded credentials in images.
- Containers MUST use minimal base images.
- Only required ports MAY be exposed.

---

## Alternatives Considered

### 1. Bare-Metal Deployment

Rejected because:
- Harder to reproduce.
- More error-prone.
- Harder to isolate dependencies.

### 2. Kubernetes

Rejected because:
- Overkill for Raspberry Pi deployment.
- Adds operational complexity.
- Violates minimal infrastructure goal.

### 3. External Managed Services

Rejected because:
- Breaks self-hosted constraint.
- Introduces external dependencies.
- Reduces portability.

---

## Consequences

### Positive

- Fully reproducible deployment.
- Minimal operational complexity.
- Clear separation of services.
- Optional infrastructure via profiles.
- Security-first default posture.

### Negative / Trade-offs

- Requires Docker knowledge.
- Compose-based orchestration is limited compared to Kubernetes.
- MQTT adds optional operational surface.

### Operational Impact

- Deployment requires Docker and Docker Compose.
- Profiles must be documented.
- Backups must include Docker volumes.
- Updates must follow migration procedures (ADR-0003).

---

## Verification

Compliance is validated by:

- CI build of all Docker images.
- Validation that containers run as non-root.
- Compose configuration review.
- Tests verifying system runs without `events` profile enabled.
- Integration tests verifying MQTT functionality when profile is enabled.

---

## Plan Enforcement

Any feature implementation plan MUST:

- Define which services are required.
- Explicitly state whether the `events` profile is needed.
- Respect LAN-only exposure rules.
- Not introduce external infrastructure dependencies.
- Define volume and persistence requirements if storage changes are involved.

If a plan violates these rules, it is invalid.