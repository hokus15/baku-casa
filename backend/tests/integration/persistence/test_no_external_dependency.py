from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.persistence_integration


def test_persistence_suite_runs_without_external_services(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )

    assert response.status_code == 201
