import time
import uuid
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app


def test_completed_transaction_triggers_background_scoring() -> None:
    with TestClient(app) as client:
        email = f"background_{uuid.uuid4().hex[:8]}@example.com"

        customer_response = client.post(
            "/api/v1/customers",
            json={
                "first_name": "Background",
                "last_name": "Test",
                "email": email,
            },
        )

        assert customer_response.status_code == 201

        customer_id = customer_response.json()["id"]

        transaction_response = client.post(
            f"/api/v1/transactions/customers/{customer_id}",
            headers={
                "Idempotency-Key": f"background-{uuid.uuid4()}",
            },
            json={
                "amount": "100.00",
                "currency": "EUR",
                "category": "GROCERIES",
                "status": "COMPLETED",
                "timestamp": "2026-09-06T12:00:00Z",
            },
        )

        assert transaction_response.status_code == 201

        deadline = time.monotonic() + 5

        while time.monotonic() < deadline:
            customer_360_response = client.get(
                f"/api/v1/customers/{customer_id}/360"
            )

            assert customer_360_response.status_code == 200

            data = customer_360_response.json()

            if Decimal(data["score"]["score"]) == Decimal("55.00"):
                return

            time.sleep(0.05)

        raise AssertionError(
            "Background scoring did not produce the expected score "
            "within 5 seconds."
        )