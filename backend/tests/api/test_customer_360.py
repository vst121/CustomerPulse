import uuid
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app


def test_get_customer_360() -> None:
    with TestClient(app) as client:
        email = f"customer360_{uuid.uuid4().hex[:8]}@example.com"

        customer_response = client.post(
            "/api/v1/customers",
            json={
                "first_name": "Customer",
                "last_name": "360",
                "email": email,
            },
        )

        assert customer_response.status_code in (200, 201)

        customer_id = customer_response.json()["id"]

        transaction_response = client.post(
            f"/api/v1/transactions/customers/{customer_id}",
            headers={
                "Idempotency-Key": f"customer360-{uuid.uuid4()}",
            },
            json={
                "amount": "100.00",
                "currency": "EUR",
                "category": "GROCERIES",
                "status": "COMPLETED",
                "timestamp": "2026-09-06T12:00:00Z",
            },
        )

        assert transaction_response.status_code in (200, 201)

        score_response = client.get(
            f"/api/v1/customers/{customer_id}/scores"
        )

        assert score_response.status_code in (200, 201)

        recommendation_response = client.post(
            f"/api/v1/customers/{customer_id}/recommendations/generate"
        )

        assert recommendation_response.status_code in (200, 201)

        response = client.get(
            f"/api/v1/customers/{customer_id}/360"
        )

        assert response.status_code in (200, 201)

        data = response.json()

        assert data["id"] == customer_id

        assert Decimal(
            data["value"]["total_spend"]
        ) == Decimal("100.00")

        assert data["value"]["transaction_count"] == 1

        assert Decimal(
            data["score"]["score"]
        ) == Decimal("55.00")

        assert len(data["transactions"]) == 1

        assert len(data["recommendations"]) == 1

        assert (
            data["recommendations"][0]["type"]
            == "CROSS_SELL"
        )