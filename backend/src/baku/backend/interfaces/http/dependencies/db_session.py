"""Abstract session dependency stub (ADR-0002).

The concrete generator is provided by infrastructure via
app.dependency_overrides in the composition root (main.py).
Repo stubs in repo_deps.py declare Depends(get_session) so all repos
that share a request always receive the same underlying session instance
(FastAPI caches the resolved value once per request).
"""

from __future__ import annotations

from collections.abc import Generator


def get_session() -> Generator[object, None, None]:
    """Abstract stub — overridden at composition root.

    Yields a database session.  Typed as Generator[object, ...] so that
    the interfaces layer imports no SQLAlchemy symbols.
    """
    raise NotImplementedError("get_session not wired — add app.dependency_overrides[get_session] in main.py")
    yield  # make this a generator even as a stub so FastAPI treats it correctly
