import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_customer() -> None:

    randomPart = uuid.uuid4().hex[:8];

    response = client.post(
        "/api/v1/customers",
        json={            
            "first_name": "Anna",
            "last_name": "Müller",
            "email": f"anna_{randomPart}@example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["first_name"] == "Anna"
    assert data["last_name"] == "Müller"
    assert data["email"] == f"anna_{randomPart}@example.com"
    assert data["lifecycle_stage"] == "ACQUISITION"