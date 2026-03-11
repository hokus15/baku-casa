"""Bootstrap lifespan — centralized configuration and fail-fast initialization (ADR-0013).

Encapsulates the startup sequence previously inline in main.py:
  1. Load and validate centralized configuration (fail-fast if required keys missing).
  2. Derive auth settings from the validated configuration profile.
  3. Derive pagination settings from the validated configuration profile.
  4. Configure framework logging.

Responsibility: LIFESPAN_BOOTSTRAP (BootstrapInventory)
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from baku.backend.infrastructure.config.auth_settings import init_auth_settings
from baku.backend.infrastructure.config.pagination_settings import init_pagination_settings
from baku.backend.infrastructure.config.runtime_settings import RuntimeConfigurationProvider
from baku.backend.infrastructure.logging.bootstrap import configure_framework_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler with fail-fast bootstrap (ADR-0013).

    Startup sequence:
      1. Load and validate centralized configuration; aborts if required
         keys are missing (aggregated error report, ADR-0013).
      2. Derive auth settings from the validated configuration profile.
      3. Derive pagination settings from the validated configuration profile;
         aborts if values are not integers or violate invariants (>= 1,
         max_page_size >= default_page_size).
      4. Configure framework logging baseline.

    Validation is deferred to the lifespan handler so that the module can be
    imported in test suites before fixtures have set the required env vars.
    """
    provider = RuntimeConfigurationProvider()
    provider.get_profile()  # fail-fast: aborts if required keys missing
    init_auth_settings(provider)
    init_pagination_settings(provider)
    configure_framework_logging()
    yield
