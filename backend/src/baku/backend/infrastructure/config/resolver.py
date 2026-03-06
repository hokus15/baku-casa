"""Deterministic precedence resolver for the centralized configuration system.

Precedence (highest → lowest):
  1. env   — process environment variables
  2. file  — .env file values
  3. default — built-in application defaults

The resolver is a pure function: given the three source dicts it returns an
immutable ``ResolvedConfigurationProfile``.  Source loading is handled by
``sources.py``; validation is handled by ``validator.py``.
"""

from __future__ import annotations

from baku.backend.application.configuration.models import ResolvedConfigurationProfile


def resolve(
    env_source: dict[str, str],
    file_source: dict[str, str],
    default_source: dict[str, str],
) -> ResolvedConfigurationProfile:
    """Merge three source dicts into a single resolved profile.

    Later sources only fill keys absent from earlier (higher-precedence) ones.
    The ``source_map`` records which source each resolved key came from.

    Args:
        env_source: Values loaded from process environment (highest precedence).
        file_source: Values loaded from .env file.
        default_source: Built-in default values (lowest precedence).

    Returns:
        An immutable ``ResolvedConfigurationProfile`` with fully merged values
        and a per-key source attribution.
    """
    values: dict[str, str] = {}
    source_map: dict[str, str] = {}

    for key, value in env_source.items():
        values[key] = value
        source_map[key] = "env"

    for key, value in file_source.items():
        if key not in values:
            values[key] = value
            source_map[key] = "file"

    for key, value in default_source.items():
        if key not in values:
            values[key] = value
            source_map[key] = "default"

    return ResolvedConfigurationProfile(values=values, source_map=source_map)
