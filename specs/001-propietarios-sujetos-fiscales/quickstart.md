# Quickstart - F-0002 Propietarios (Sujetos Fiscales)

## Objective

Validate owner master-data workflows end-to-end: create, retrieve, list/search, update, and soft delete with auditability and authentication.

## Preconditions

- Run from `backend` root with test/development configuration loaded.
- Authentication flow from F-0001 available.
- Empty or controlled database state for deterministic checks.

## Manual validation flow

1. Authenticate operator
  - Obtain JWT using existing auth endpoint.
  - Use token for all owner requests.

2. Create owner
  - Create owner with required identity and address fields (`entity_type`, `first_name`, `last_name`, `legal_name`, `tax_id`, fiscal address).
  - Optionally include `stamp_image` and verify persistence when provided.
  - Verify `entity_type` accepts only `PERSONA_FISICA`, `PERSONA_JURIDICA`, `ESPJ`.
  - Create owner with optional contact fields (`email`, `land_line`, `land_line_country_code`, `mobile`, `mobile_country_code`) and verify persistence.
  - Omit `fiscal_address_country` and verify default `ES`.
  - Omit `land_line_country_code` and/or `mobile_country_code` and verify default `34` when `land_line` or `mobile` is provided.
  - Verify audit fields (`created_at`, `created_by`, `updated_at`, `updated_by`) are present.

3. Verify tax_id normalization
  - Attempt second create with formatting variant of same tax_id (spaces/hyphens/case differences).
  - Verify conflict response due to normalized uniqueness.

4. Detail retrieval
  - Read owner by `owner_id` and verify full representation.

5. List and search
  - List owners with pagination defaults.
  - Filter by exact normalized tax_id.
  - Filter by partial `legal_name`.
  - Verify `include_deleted` behavior in list.

6. Update owner
  - Update editable fields and verify `updated_at`/`updated_by` changes.
  - Attempt to modify `owner_id` and verify request is rejected (or ignored with immutable persisted value).

7. Soft delete owner
  - Delete owner and verify `deleted_at` and `deleted_by` are set.
  - Verify deleted owner is absent from default list/detail.
  - Verify deleted owner appears when `include_deleted = true` in both list and detail.

8. Error and logging checks
  - Verify typed errors (`VALIDATION_ERROR`, `NOT_FOUND`, `CONFLICT`, auth failures) include `correlation_id`.
  - Verify logs include `correlation_id` but exclude owner PII fields.

## Contract and CI validation

Expected CI quality gates for this feature:

- `ruff check src/ tests/`
- `mypy src/`
- `pytest tests/ -q`

Contract tests must cover:

- create success and duplicate tax_id conflict
- invalid `entity_type` enum and missing required fields (`first_name`, `last_name` included)
- list/search pagination and filters
- include_deleted behavior in list + detail
- update immutability and conflict handling
- soft delete and repeated delete behavior
- unauthenticated access on all endpoints

## Implementation evidence (automated validation)

**Executed**: v1.0 implementation completed and all quality gates passed.

### Quality gate results

```
ruff check src/ tests/   →  All checks passed!
mypy src/                →  Success: no issues found in 93 source files
pytest tests/ -q         →  176 passed, 3 warnings in 104.50s
```

### Test coverage by scenario

| Scenario | Test file |
|---|---|
| Create owner — success | `tests/contract/owners/test_create_owner_contract.py` |
| Create owner — duplicate tax_id | `tests/contract/owners/test_create_owner_contract.py` |
| Create owner — validation errors | `tests/contract/owners/test_create_owner_contract.py` |
| List owners — pagination | `tests/integration/owners/test_list_owners_pagination.py` |
| List owners — filters (legal_name, tax_id, include_deleted) | `tests/integration/owners/test_list_owners_filters.py` |
| Get owner by ID — detail | `tests/integration/owners/test_get_owner_detail_flow.py` |
| tax_id normalization + conflict detection | `tests/integration/owners/test_tax_id_normalization.py` |
| Update owner — PATCH fields + conflict | `tests/integration/owners/test_update_owner_conflict.py` |
| Soft delete + auditability | `tests/integration/owners/test_soft_delete_owner_flow.py` |
| Second delete returns 404 (OwnerNotFound) | `tests/integration/owners/test_soft_delete_owner_idempotency.py` |

All 5 contract test files and 8 integration test files pass with 55 owners-specific tests total (within the 176-test suite).
