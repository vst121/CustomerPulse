import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_completed_transaction_updates_customer_value() -> None:
    email = f"value_flow_{uuid.uuid4().hex[:8]}@example.com"

    # 1. Create customer
    customer_response = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Value",
            "last_name": "Flow",
            "email": email,
        },
    )

    assert customer_response.status_code == 201

    customer_id = customer_response.json()["id"]

    # 2. Create completed transaction
    transaction_response = client.post(
        f"/api/v1/transactions/customers/{customer_id}",
        headers={
            "Idempotency-Key": f"value-flow-{uuid.uuid4()}",
        },
        json={
            "amount": "250.00",
            "currency": "EUR",
            "category": "SHOPPING",
            "status": "COMPLETED",
            "timestamp": "2026-09-06T20:00:00Z",
        },
    )

    assert transaction_response.status_code == 201

    # 3. Read Customer 360
    response = client.get(
        f"/api/v1/customers/{customer_id}/360"
    )

    assert response.status_code == 200

    data = response.json()

    # 4. Verify transaction
    assert len(data["transactions"]) == 1
    assert data["transactions"][0]["status"] == "COMPLETED"

    # 5. Verify Customer Value
    assert data["value"]["total_spend"] == "250.00"
    assert data["value"]["transaction_count"] == 1