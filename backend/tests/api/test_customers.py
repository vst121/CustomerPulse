from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_customer() -> None:

    response = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Anna",
            "last_name": "Müller",
            "email": "anna.test@example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["first_name"] == "Anna"
    assert data["last_name"] == "Müller"
    assert data["email"] == "anna.test@example.com"
    assert data["lifecycle_stage"] == "ACQUISITION"