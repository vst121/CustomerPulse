import uuid
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app


def test_customer_score_drives_recommendation() -> None:
    with TestClient(app) as client:
        email = (
            f"decision_{uuid.uuid4().hex[:8]}"
            "@example.com"
        )

        customer_response = client.post(
            "/api/v1/customers",
            json={
                "first_name": "Decision",
                "last_name": "Test",
                "email": email,
            },
        )

        assert customer_response.status_code in (200, 201)

        customer_id = customer_response.json()["id"]

        transaction_response = client.post(
            f"/api/v1/transactions/customers/{customer_id}",
            headers={
                "Idempotency-Key": f"decision-{uuid.uuid4()}",
            },
            json={
                "amount": "120.00",
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

        score_data = score_response.json()

        assert Decimal(
            score_data["score"]
        ) == Decimal("65.00")

        recommendation_response = client.post(
            f"/api/v1/customers/{customer_id}/recommendations/generate"
        )

        assert recommendation_response.status_code in (200, 201)

        recommendation_data = recommendation_response.json()

        assert (
            recommendation_data["type"]
            == "UPSELL"
        )

        customer_360_response = client.get(
            f"/api/v1/customers/{customer_id}/360"
        )

        assert customer_360_response.status_code in (200, 201)

        customer_360_data = customer_360_response.json()

        assert Decimal(
            customer_360_data["score"]["score"]
        ) == Decimal("65.00")

        assert len(
            customer_360_data["recommendations"]
        ) == 1

        assert (
            customer_360_data["recommendations"][0]["type"]
            == "UPSELL"
        )