"""Integration test: bootstrap responsibility separation (US1).

Verifies that each bootstrap responsibility is separated into its dedicated
module as defined in the Bootstrap Responsibility Inventory (spec FR-002, SC-001).

Every item in BootstrapInventory must have a corresponding module with the
expected callable, and the closed set must match exactly.
"""

from __future__ import annotations


def test_lifespan_module_has_lifespan_handler() -> None:
    """lifespan.py must expose a 'lifespan' async context manager."""
    from baku.backend.interfaces.http.bootstrap import lifespan as lifespan_mod

    assert hasattr(lifespan_mod, "lifespan"), "lifespan.py must define 'lifespan'"
    assert callable(lifespan_mod.lifespan)


def test_app_factory_module_has_create_app() -> None:
    """app_factory.py must expose 'create_app' callable."""
    from baku.backend.interfaces.http.bootstrap import app_factory

    assert hasattr(app_factory, "create_app"), "app_factory.py must define 'create_app'"
    assert callable(app_factory.create_app)


def test_dependency_wiring_module_has_wire_dependencies() -> None:
    """dependency_wiring.py must expose 'wire_dependencies' callable."""
    from baku.backend.interfaces.http.bootstrap import dependency_wiring

    assert hasattr(dependency_wiring, "wire_dependencies"), "dependency_wiring.py must define 'wire_dependencies'"
    assert callable(dependency_wiring.wire_dependencies)


def test_middleware_registry_module_has_register_middleware() -> None:
    """middleware_registry.py must expose 'register_middleware' callable."""
    from baku.backend.interfaces.http.bootstrap import middleware_registry

    assert hasattr(
        middleware_registry, "register_middleware"
    ), "middleware_registry.py must define 'register_middleware'"
    assert callable(middleware_registry.register_middleware)


def test_error_handlers_registry_module_has_register_error_handlers() -> None:
    """error_handlers_registry.py must expose 'register_error_handlers' callable."""
    from baku.backend.interfaces.http.bootstrap import error_handlers_registry

    assert hasattr(
        error_handlers_registry, "register_error_handlers"
    ), "error_handlers_registry.py must define 'register_error_handlers'"
    assert callable(error_handlers_registry.register_error_handlers)


def test_router_registry_module_has_register_routers() -> None:
    """router_registry.py must expose 'register_routers' callable."""
    from baku.backend.interfaces.http.bootstrap import router_registry

    assert hasattr(router_registry, "register_routers"), "router_registry.py must define 'register_routers'"
    assert callable(router_registry.register_routers)


def test_bootstrap_inventory_closed_set_matches_spec() -> None:
    """BootstrapInventory must enumerate exactly the 6 responsibilities from spec FR-002."""
    from baku.backend.interfaces.http.bootstrap.contracts import BootstrapInventory

    expected = {
        "APP_CREATION",
        "LIFESPAN_BOOTSTRAP",
        "DEPENDENCY_COMPOSITION_WIRING",
        "MIDDLEWARE_REGISTRATION",
        "ERROR_HANDLERS_REGISTRATION",
        "ROUTER_REGISTRATION",
    }
    actual = {item.name for item in BootstrapInventory}
    assert actual == expected, f"BootstrapInventory mismatch. Expected: {expected}, Got: {actual}"


def test_bootstrap_package_exports_create_app_and_inventory() -> None:
    """The bootstrap __init__.py must export create_app and BootstrapInventory."""
    import baku.backend.interfaces.http.bootstrap as bootstrap_pkg

    assert hasattr(bootstrap_pkg, "create_app"), "bootstrap package must export 'create_app'"
    assert hasattr(bootstrap_pkg, "BootstrapInventory"), "bootstrap package must export 'BootstrapInventory'"
