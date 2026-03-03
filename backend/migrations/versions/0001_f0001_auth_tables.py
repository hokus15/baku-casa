"""Migration 0001 — F-0001 auth tables.

Creates tables: operators, revoked_tokens, login_throttle_states.
Applied automatically via SQLAlchemy create_all in db.py.
This file documents the intended schema for traceability (ADR-0003).

DDL (equivalent SQL):

    CREATE TABLE operators (
        operator_id   TEXT        PRIMARY KEY,
        username      TEXT        NOT NULL UNIQUE,
        password_hash TEXT        NOT NULL,
        credential_version INTEGER NOT NULL DEFAULT 1,
        created_at    TEXT        NOT NULL,
        updated_at    TEXT,
        last_login_at TEXT,
        is_active     INTEGER     NOT NULL DEFAULT 1
    );

    CREATE TABLE revoked_tokens (
        token_jti   TEXT PRIMARY KEY,
        operator_id TEXT NOT NULL REFERENCES operators(operator_id),
        revoked_at  TEXT NOT NULL,
        expires_at  TEXT NOT NULL,
        reason      TEXT NOT NULL
    );

    CREATE TABLE login_throttle_states (
        operator_id     TEXT PRIMARY KEY REFERENCES operators(operator_id),
        failed_attempts INTEGER NOT NULL DEFAULT 0,
        blocked_until   TEXT,
        last_failed_at  TEXT
    );

All timestamps stored as ISO 8601 UTC strings (ADR-0012).
"""

MIGRATION_ID = "0001_f0001_auth_tables"
DESCRIPTION = "Create authentication tables for F-0001"
