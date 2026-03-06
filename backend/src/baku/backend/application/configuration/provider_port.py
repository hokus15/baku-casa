"""Centralized configuration provider port (EN-0202 / ADR-0013).

Application layer port — infrastructure must implement this interface.
Domain layer must NOT import from this module (ADR-0002).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from baku.backend.application.configuration.models import ResolvedConfigurationProfile


class ConfigurationProviderPort(ABC):
    """Port for accessing the fully-resolved, validated configuration profile.

    The single concrete implementation lives in the Infrastructure layer
    (``infrastructure.config.runtime_settings``).  The composition root
    (``main.py``) is the primary module that imports the concrete class and
    injects it via ``init_auth_settings()`` and similar entry points; other
    Infrastructure modules depend only on this port.

    Usage::

        profile = provider.get_profile()
        secret = profile.require("auth.jwt_secret")
    """

    @abstractmethod
    def get_profile(self) -> ResolvedConfigurationProfile:
        """Return the validated configuration profile for the running process.

        The profile is resolved once at startup and cached for the lifetime
        of the process.  Calling this method multiple times is safe.

        Raises:
            AggregatedConfigurationError: if the profile has not yet been
                successfully validated (i.e. startup validation was skipped).
        """
