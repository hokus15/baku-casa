"""Bootstrap boundary contracts — structural type definitions for the HTTP bootstrap module.

Defines the closed set of bootstrap responsibilities (spec FR-002, SC-001, SC-004).
Every responsibility in the inventory must be assigned to exactly one bootstrap
component. No additional responsibility may be retained in the entrypoint (main.py).
"""

from __future__ import annotations

from enum import Enum


class BootstrapInventory(str, Enum):
    """Closed set of bootstrap responsibilities (spec FR-002, SC-001, SC-004).

    Mapping to modules:
      APP_CREATION                  -> app_factory.py
      LIFESPAN_BOOTSTRAP            -> lifespan.py
      DEPENDENCY_COMPOSITION_WIRING -> dependency_wiring.py
      MIDDLEWARE_REGISTRATION       -> middleware_registry.py
      ERROR_HANDLERS_REGISTRATION   -> error_handlers_registry.py
      ROUTER_REGISTRATION           -> router_registry.py
    """

    APP_CREATION = "app_creation"
    LIFESPAN_BOOTSTRAP = "lifespan_bootstrap"
    DEPENDENCY_COMPOSITION_WIRING = "dependency_composition_wiring"
    MIDDLEWARE_REGISTRATION = "middleware_registration"
    ERROR_HANDLERS_REGISTRATION = "error_handlers_registration"
    ROUTER_REGISTRATION = "router_registration"
