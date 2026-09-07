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

def test_get_customer_intelligence() -> None:
    with TestClient(app) as client:
        email = (
            f"intelligence_{uuid.uuid4().hex[:8]}@example.com"
        )

        customer_response = client.post(
            "/api/v1/customers",
            json={
                "first_name": "Customer",
                "last_name": "Intelligence",
                "email": email,
            },
        )

        assert customer_response.status_code in (200, 201)

        customer_id = customer_response.json()["id"]

        transaction_response = client.post(
            f"/api/v1/transactions/customers/{customer_id}",
            headers={
                "Idempotency-Key": f"intelligence-{uuid.uuid4()}",
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

        response = client.get(
            f"/api/v1/customers/{customer_id}/intelligence"
        )

        assert response.status_code == 200

        data = response.json()

        assert data["features"]["transaction_count"] == 1

        assert Decimal(
            data["features"]["total_transaction_value"]
        ) == Decimal("100.00")

        assert Decimal(
            data["features"]["average_transaction_value"]
        ) == Decimal("100.00")

        assert data["features"]["days_since_last_transaction"] >= 0

        assert Decimal(
            data["prediction"]["churn_probability"]
        ) == Decimal("0.20")

        assert data["action"]["action_type"] == "GROWTH_OFFER"
        assert data["action"]["priority"] == 3

        assert (
            data["action"]["reason"]
            == "Customer has low churn risk and may be suitable for growth."
        )