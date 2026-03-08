# Error Contract - Owners (F-0002)

## General rules

- `error_code`: stable machine-readable code in English.
- `message`: descriptive message in Spanish.
- Error descriptions in API contracts and documentation: Spanish.
- `correlation_id`: required in every error response.

## Expected functional error codes

- `OWNER_VALIDATION_ERROR`
- `OWNER_NOT_FOUND`
- `OWNER_TAX_ID_CONFLICT`
- `OWNER_IMMUTABLE_ID`
- `AUTH_UNAUTHORIZED`

## Expected HTTP mapping

- `400`: payload/query validation errors and immutable-field violations.
- `401`: missing/invalid/expired authentication token.
- `404`: owner does not exist or is soft-deleted while `include_deleted = false`.
- `409`: active-owner conflict on normalized tax_id uniqueness.

## Notes

- Error code stability is required within MAJOR `v1`.
- Error payloads must include `correlation_id` for traceability.
- Logging of errors must not include owner PII values.
