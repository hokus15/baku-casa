"""Integration test: thin HTTP entrypoint boundary (US1).

Verifies that main.py remains bounded to delegation only:
  - No direct infrastructure imports (ADR-0002 composition root in bootstrap module)
  - app is produced by create_app() from the bootstrap module
  - main.py does not construct FastAPI directly
  - main.py does not register middleware, routers, or error handlers directly

Spec: FR-001 — entry point bounded to initialization delegation.
"""

from __future__ import annotations

import inspect


def test_main_module_exposes_app_instance() -> None:
    """main.py must expose an 'app' FastAPI instance."""
    from fastapi import FastAPI

    from baku.backend.main import app

    assert isinstance(app, FastAPI)


def test_main_module_delegates_to_create_app() -> None:
    """main.py must delegate app construction to create_app() from bootstrap module."""
    import baku.backend.main as main_module

    source = inspect.getsource(main_module)
    assert "create_app" in source, "main.py must call create_app() from bootstrap module"


def test_main_module_does_not_construct_fastapi_directly() -> None:
    """main.py must not contain a FastAPI() constructor call."""
    import baku.backend.main as main_module

    source = inspect.getsource(main_module)
    assert "FastAPI(" not in source, "main.py must not construct FastAPI directly; delegate to create_app()"


def test_main_module_has_no_direct_infrastructure_imports() -> None:
    """main.py must not import from the infrastructure layer directly (ADR-0002)."""
    import baku.backend.main as main_module

    source = inspect.getsource(main_module)
    assert (
        "baku.backend.infrastructure" not in source
    ), "main.py must not import from infrastructure; infrastructure is wired in dependency_wiring.py"


def test_main_module_does_not_register_middleware_directly() -> None:
    """main.py must not call add_middleware() directly."""
    import baku.backend.main as main_module

    source = inspect.getsource(main_module)
    assert "add_middleware" not in source, "Middleware registration must be in middleware_registry.py"


def test_main_module_does_not_register_routers_directly() -> None:
    """main.py must not call include_router() directly."""
    import baku.backend.main as main_module

    source = inspect.getsource(main_module)
    assert "include_router" not in source, "Router registration must be in router_registry.py"


def test_main_module_does_not_wire_dependencies_directly() -> None:
    """main.py must not touch dependency_overrides directly."""
    import baku.backend.main as main_module

    source = inspect.getsource(main_module)
    assert "dependency_overrides" not in source, "Dependency wiring must be in dependency_wiring.py"
