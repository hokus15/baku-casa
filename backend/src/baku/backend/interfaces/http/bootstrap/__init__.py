"""HTTP Bootstrap module — EN-0300.

Exports the public interface for bootstrap traceability:
  - create_app: factory function; single entry point for app construction
  - BootstrapInventory: closed enum of all bootstrap responsibilities (spec FR-002)
"""

from __future__ import annotations

from baku.backend.interfaces.http.bootstrap.app_factory import create_app
from baku.backend.interfaces.http.bootstrap.contracts import BootstrapInventory

__all__ = ["create_app", "BootstrapInventory"]
