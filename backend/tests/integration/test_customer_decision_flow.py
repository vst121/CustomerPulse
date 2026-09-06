import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_customer_score_drives_recommendation() -> None:
    email = f"decision_flow_{uuid.uuid4().hex[:8]}@example.com"

    # 1. Create customer
    customer_response = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Decision",
            "last_name": "Flow",
            "email": email,
        },
    )

    assert customer_response.status_code in (200, 201)

    customer_id = customer_response.json()["id"]

    # 2. Create completed transaction
    transaction_response = client.post(
        f"/api/v1/transactions/customers/{customer_id}",
        headers={
            "Idempotency-Key": f"decision-flow-{uuid.uuid4()}",
        },
        json={
            "amount": "120.00",
            "currency": "EUR",
            "category": "SHOPPING",
            "status": "COMPLETED",
            "timestamp": "2026-09-06T20:00:00Z",
        },
    )

    assert transaction_response.status_code in (200, 201)

    # 3. Calculate score
    score_response = client.get(
        f"/api/v1/customers/{customer_id}/scores"
    )

    assert score_response.status_code in (200, 201)

    score = score_response.json()["score"]

    # 120 * 0.5 + 1 * 5 = 65
    assert float(score) == 65.0

    # 4. Generate recommendation
    recommendation_response = client.post(
        f"/api/v1/customers/{customer_id}/recommendations/generate"
    )

    assert recommendation_response.status_code in (200, 201)

    recommendation = recommendation_response.json()

    # Score >= 60 → UPSELL
    assert recommendation["type"] == "UPSELL"
    assert recommendation["customer_id"] == customer_id

    # 5. Verify through Customer 360
    customer_360_response = client.get(
        f"/api/v1/customers/{customer_id}/360"
    )

    assert customer_360_response.status_code in (200, 201)

    data = customer_360_response.json()

    assert float(data["score"]["score"]) == 65.0
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["type"] == "UPSELL"