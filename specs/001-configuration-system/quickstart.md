# Quickstart - EN-0202 Configuration System

## Objective
Validate the EN-0202 behavior end-to-end for deterministic configuration resolution and fail-fast startup validation.

## Preconditions
- Work on branch `001-configuration-system`.
- `backend/` dependencies installed.
- Test environment isolated from production data.

## Validation Flow

1. Baseline valid startup
- Provide required global keys with valid values.
- Start backend.
- Expected: startup succeeds with resolved configuration profile.

2. Source precedence validation
- Define same key in environment, config file, and defaults.
- Start backend in each target environment (`dev`, `test`, `prod`).
- Expected: winner is always `environment variables > config file > defaults`.

3. Missing/invalid required values
- Remove one required key and set another with invalid format/range.
- Start backend.
- Expected: startup fails and reports complete set of validation issues in one run.

4. Unknown keys handling
- Add undeclared keys in environment/config file.
- Start backend with otherwise valid required keys.
- Expected: startup succeeds; warnings are emitted for undeclared keys.

5. Test environment isolation
- Validate that `test` profile does not point to non-test persistent resources.
- Expected: configuration profile for `test` remains explicitly isolated.

6. F-0001 compatibility regression
- Validate that existing authentication-related configuration remains effective after centralization.
- Expected: token TTL and lockout policy parameters keep prior functional behavior defined by `F-0001`.

## Evidence Checklist
- Deterministic precedence behavior captured.
- Aggregated validation errors captured.
- Warning behavior for undeclared keys captured.
- F-0001 configuration compatibility evidence captured.
- No external contract changes confirmed.
- CI gates impacted and passing: lint, type-check, unit/integration tests relevant to EN-0202.

## Implementation Evidence (2026-03-06)

### Test Results
- **64/64 tests passed** (0 failed, 0 skipped) — full suite, including 30 new EN-0202 tests and all F-0001 regression tests.
- New test modules:
  - `tests/integration/configuration/test_startup_valid_config.py` (5 tests)
  - `tests/integration/configuration/test_precedence_resolution.py` (5 tests)
  - `tests/integration/configuration/test_missing_required_config.py` (3 tests)
  - `tests/integration/configuration/test_aggregated_validation_errors.py` (4 tests)
  - `tests/integration/configuration/test_unknown_keys_warning.py` (4 tests)
  - `tests/integration/configuration/test_test_profile_isolation.py` (4 tests)
  - `tests/integration/auth/test_auth_config_compatibility.py` (5 tests)

### Quality Gates
- `ruff check src/ tests/` — **All checks passed**
- `mypy src/ --ignore-missing-imports` — **Success: no issues found in 60 source files**
- `pytest tests/` — **64 passed, 3 warnings** (warnings are expected `UserWarning` from undeclared-key tests)

### Key Implementation Files
- `application/configuration/models.py` — typed models (ConfigurationParameterDefinition, ResolvedConfigurationProfile, ConfigurationValidationIssue)
- `application/configuration/errors.py` — typed error types (AggregatedConfigurationError, MissingRequiredKeyError)
- `application/configuration/provider_port.py` — ConfigurationProviderPort abstract base
- `infrastructure/config/sources.py` — env/file/default source loaders; sole location of `os.environ` access (ADR-0013)
- `infrastructure/config/resolver.py` — deterministic `env > file > default` precedence
- `infrastructure/config/validator.py` — fail-fast aggregated validator with undeclared-key warnings
- `infrastructure/config/runtime_settings.py` — RuntimeConfigurationProvider (concrete implementation + singleton)
- `infrastructure/config/auth_settings.py` — refactored to consume centralized provider (no direct `os.getenv`)
- `main.py` — centralized config validated at module load before routers are included
