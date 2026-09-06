import uuid
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_customer_360() -> None:
    email = f"customer360_{uuid.uuid4().hex[:8]}@example.com"

    # 1. Create customer
    customer_response = client.post(
        "/api/v1/customers",
        json={
            "first_name": "John",
            "last_name": "Customer360",
            "email": email,
        },
    )

    assert customer_response.status_code == 201

    customer = customer_response.json()
    customer_id = customer["id"]

    # 2. Create transaction
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

    # 3. Calculate customer score
    score_response = client.get(
        f"/api/v1/customers/{customer_id}/scores"
    )

    assert score_response.status_code in (200, 201)

    # 4. Generate recommendation
    recommendation_response = client.post(
        f"/api/v1/customers/{customer_id}/recommendations/generate"
    )

    assert recommendation_response.status_code in (200, 201)

    # 5. Get Customer 360
    response = client.get(
        f"/api/v1/customers/{customer_id}/360"
    )

    assert response.status_code in (200, 201)

    data = response.json()

    # Customer
    assert data["id"] == customer_id
    assert data["first_name"] == "John"
    assert data["last_name"] == "Customer360"
    assert data["email"] == email
    assert data["lifecycle_stage"] == "ACQUISITION"

    # Customer Value
    assert Decimal(data["value"]["total_spend"]) == Decimal("100.00")
    assert data["value"]["transaction_count"] == 1

    # Customer Score
    assert Decimal(data["score"]["score"]) == Decimal("55.00")

    # Transactions
    assert len(data["transactions"]) == 1

    transaction = data["transactions"][0]

    assert Decimal(transaction["amount"]) == Decimal("100.00")
    assert transaction["currency"] == "EUR"
    assert transaction["category"] == "GROCERIES"
    assert transaction["status"] == "COMPLETED"

    # Recommendations
    assert len(data["recommendations"]) == 1

    recommendation = data["recommendations"][0]

    assert recommendation["type"] == "CROSS_SELL"