# ADR-0005: Authentication Strategy (Stateless JWT + Revocation Without Server-Side Sessions)

## Status
Accepted

## Context

The system requires authenticated access to its HTTP API from the earliest features.

Key drivers and constraints:

- Self-hosted deployment on constrained hardware (e.g., Raspberry Pi).
- No external services (e.g., Redis) for session storage.
- Support for configurable token TTLs, including long-lived tokens.
- Security requirement: when a user changes their password, all tokens issued under the previous credentials MUST be revoked.
- The architecture requires strict separation of concerns (see ADR-0002) and stable API contracts (see ADR-0004).

A stateless authentication mechanism is required, with a revocation strategy that does not depend on external session stores.


## Decision

The system SHALL use **JWT (JSON Web Tokens)** for authentication with a **stateless** validation model, augmented by a **credential epoch** (a.k.a. token version) mechanism to support revocation.

### Token Model (Binding)

- Access tokens MUST be JWTs signed with a server-controlled secret.
- Tokens MUST include at minimum:
  - `sub` (user identifier)
  - `iat` (issued-at)
  - `exp` (expiration)
  - `jti` (unique token id)
  - `ver` (credential version / epoch)

- Token TTL MUST be configurable.
- Long-lived tokens are allowed, but MUST still include `exp`.

### Revocation Strategy (No Redis)

- Each user record MUST include a persistent integer `credential_version` (or equivalent) stored in the database.
- On password change (and any forced logout/security event), `credential_version` MUST be incremented atomically.
- During authentication, the system MUST verify:
  - token signature
  - `exp` validity
  - user existence and active status
  - `token.ver == user.credential_version`

If the versions do not match, the token MUST be rejected as revoked.

This guarantees that all previously issued tokens become invalid immediately after the version increment, without requiring server-side session storage.

### Optional Token Blacklist (Bounded)

- A persistent blacklist MAY be implemented using the database for targeted revocation (e.g., per `jti`), but it MUST be:
  - bounded in size via TTL cleanup
  - optional, not required for correctness

### Authorization (Scope)

- Authentication (who you are) is handled by JWT validation.
- Authorization (roles/permissions, RBAC/ACL) is explicitly out of scope for the initial enable.
- The system SHALL assume a single-user model for MVP/Enable 1.
- If authorization is introduced in the future, it MUST be implemented at the application boundary and MUST NOT be embedded as business logic in HTTP controllers.

### Security Practices

- Secrets MUST be loaded via configuration/secrets management (not hard-coded).
- JWT algorithms MUST be explicitly restricted to the intended algorithm(s).
- Clock skew handling MUST be bounded and explicit.
- Error responses MUST NOT leak sensitive information (e.g., whether a user exists).


This decision is normative and binding.


## Alternatives Considered

### 1. Server-Side Sessions (Redis)

Rejected because:
- Violates the “no external services” constraint.
- Adds operational overhead and complexity.
- Reduces portability and lightweight deployment goals.

### 2. Short-Lived Tokens Only (No Revocation Strategy)

Rejected because:
- Does not meet the requirement of immediate revocation after password changes.
- Forces impractically short TTLs and worse UX.

### 3. Pure JWT Without Versioning (Stateless Only)

Rejected because:
- Cannot revoke previously issued tokens without server-side state.
- Violates the password-change revocation requirement.

### 4. Database-Backed Session Store

Rejected as the primary approach because:
- Reintroduces session semantics and lookup for every request.
- Adds complexity comparable to Redis-based sessions.
Kept only as an optional bounded blacklist for targeted revocation (jti).


## Consequences

### Positive

- Stateless tokens with immediate revocation on password changes.
- No need for Redis or external session infrastructure.
- Simple mental model and operational footprint.
- Works consistently across implementations.

### Negative / Trade-offs

- Requires a database read for user `credential_version` on authenticated requests (unless safely cached).
- Token invalidation is per-user, not per-token, unless optional blacklist is added.
- Care must be taken to increment versions atomically and handle concurrency.

### Operational Impact

- Requires schema support for `credential_version`.
- Requires secure secret handling and rotation process.
- Requires consistent clock/time configuration.

### Verification

Compliance is validated by:

- Unit tests: issuing token includes `ver`, rejects mismatched versions.
- Integration tests: password change increments version and revokes old tokens.
- Security tests: algorithm restrictions enforced, tokens without required claims rejected.
- CI checks: no controller-level business logic; auth is adapter + application boundary.


## Plan Enforcement

Any feature implementation plan MUST:

- Reference this ADR explicitly for any authenticated endpoint.
- Specify how tokens are issued and validated (claims, TTL, algorithm restriction).
- Include the password-change revocation flow (credential_version increment).
- Add/update tests proving revocation behavior.

If a plan violates these rules, it is invalid.