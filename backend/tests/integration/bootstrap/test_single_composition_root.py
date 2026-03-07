"""Integration test: single composition root enforcement (US2).

Verifies that dependency composition is centralized exclusively in
dependency_wiring.py and that main.py does not wire dependencies directly.

Spec: FR-003 — single composition root for dependency composition between layers.
ADR-0002 — only the composition root may import from both Interfaces and Infrastructure.
"""

from __future__ import annotations

import inspect


def test_dependency_wiring_is_the_composition_root() -> None:
    """dependency_wiring.py must contain wire_dependencies() as the composition root."""
    from baku.backend.interfaces.http.bootstrap import dependency_wiring

    assert callable(dependency_wiring.wire_dependencies)


def test_main_module_does_not_contain_dependency_overrides() -> None:
    """main.py must not call dependency_overrides directly (wiring delegated to bootstrap)."""
    import baku.backend.main as main_module

    source = inspect.getsource(main_module)
    assert (
        "dependency_overrides" not in source
    ), "main.py must not wire dependencies directly; use dependency_wiring.wire_dependencies()"


def test_dependency_wiring_imports_from_infrastructure() -> None:
    """dependency_wiring.py must import from infrastructure (it IS the composition root)."""
    import baku.backend.interfaces.http.bootstrap.dependency_wiring as dw_mod

    source = inspect.getsource(dw_mod)
    assert (
        "baku.backend.infrastructure" in source
    ), "dependency_wiring.py must import from infrastructure; it is the composition root (ADR-0002)"


def test_app_factory_does_not_import_infrastructure_directly() -> None:
    """app_factory.py must not import from infrastructure; it delegates to dependency_wiring."""
    import baku.backend.interfaces.http.bootstrap.app_factory as af_mod

    source = inspect.getsource(af_mod)
    assert (
        "baku.backend.infrastructure" not in source
    ), "app_factory.py must not import from infrastructure; delegation goes via dependency_wiring.py"


def test_middleware_registry_does_not_import_infrastructure() -> None:
    """middleware_registry.py must not import from infrastructure."""
    import baku.backend.interfaces.http.bootstrap.middleware_registry as mr_mod

    source = inspect.getsource(mr_mod)
    assert "baku.backend.infrastructure" not in source


def test_router_registry_does_not_import_infrastructure() -> None:
    """router_registry.py must not import from infrastructure."""
    import baku.backend.interfaces.http.bootstrap.router_registry as rr_mod

    source = inspect.getsource(rr_mod)
    assert "baku.backend.infrastructure" not in source


def test_error_handlers_registry_does_not_import_infrastructure() -> None:
    """error_handlers_registry.py must not import from infrastructure."""
    import baku.backend.interfaces.http.bootstrap.error_handlers_registry as ehr_mod

    source = inspect.getsource(ehr_mod)
    assert "baku.backend.infrastructure" not in source
