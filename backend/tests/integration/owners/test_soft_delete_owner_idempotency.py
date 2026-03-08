"""Integration tests: Soft delete idempotency — US5."""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Idempotency",
    "last_name": "Owner",
    "legal_name": "Idempotency Owner",
    "tax_id": "IDMPT001",
    "fiscal_address_line1": "Calle Idem 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def test_second_delete_returns_404(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_resp = client.post("/api/v1/owners", json=_VALID_PAYLOAD, headers=headers)
    owner_id = create_resp.json()["owner_id"]

    first = client.delete(f"/api/v1/owners/{owner_id}", headers=headers)
    assert first.status_code == 204

    second = client.delete(f"/api/v1/owners/{owner_id}", headers=headers)
    assert second.status_code == 404
    assert second.json()["error_code"] == "OWNER_NOT_FOUND"
