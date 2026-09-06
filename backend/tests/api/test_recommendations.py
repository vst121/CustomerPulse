import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_customer() -> str:
    email = f"recommendation_{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Anna",
            "last_name": "Müller",
            "email": email,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_get_customer_recommendations_for_new_customer():
    customer_id = create_customer()

    response = client.get(
        f"/api/v1/customers/{customer_id}/recommendations"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_generate_customer_recommendation():
    customer_id = create_customer()

    response = client.post(
        f"/api/v1/customers/{customer_id}/recommendations/generate"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == customer_id
    assert data["type"] == "NO_ACTION"
    assert "No immediate action" in data["reason"]


def test_generated_recommendation_appears_in_history():
    customer_id = create_customer()

    generate_response = client.post(
        f"/api/v1/customers/{customer_id}/recommendations/generate"
    )

    assert generate_response.status_code == 200

    recommendation_id = generate_response.json()["id"]

    response = client.get(
        f"/api/v1/customers/{customer_id}/recommendations"
    )

    assert response.status_code == 200

    recommendations = response.json()

    assert len(recommendations) == 1
    assert recommendations[0]["id"] == recommendation_id
    assert recommendations[0]["type"] == "NO_ACTION"