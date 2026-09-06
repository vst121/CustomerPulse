import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_customer(
    first_name: str,
    last_name: str,
) -> dict:
    email = f"{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/api/v1/customers",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_search_customers_by_name() -> None:
    create_customer("Alice", "Smith")
    create_customer("Bob", "Johnson")

    response = client.get(
        "/api/v1/customers",
        params={"search": "Alice"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    assert any(
        customer["first_name"] == "Alice"
        for customer in data["items"]
    )


def test_filter_customers_by_lifecycle_stage() -> None:
    customer = create_customer("Lifecycle", "Customer")

    response = client.get(
        "/api/v1/customers",
        params={
            "lifecycle_stage": "ACQUISITION",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1

    assert all(
        customer["lifecycle_stage"] == "ACQUISITION"
        for customer in data["items"]
    )


def test_customer_pagination() -> None:
    create_customer("Page", "One")
    create_customer("Page", "Two")
    create_customer("Page", "Three")

    response = client.get(
        "/api/v1/customers",
        params={
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) <= 2
    assert data["total"] >= 3


def test_search_and_filter_customers_together() -> None:
    create_customer("Alice", "Anderson")
    create_customer("Alice", "Brown")
    create_customer("Bob", "Alice")

    response = client.get(
        "/api/v1/customers",
        params={
            "search": "Alice",
            "lifecycle_stage": "ACQUISITION",
            "page": 1,
            "page_size": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 10

    assert data["total"] >= 2

    for customer in data["items"]:
        assert customer["lifecycle_stage"] == "ACQUISITION"

        searchable_text = (
            f"{customer['first_name']} "
            f"{customer['last_name']} "
            f"{customer['email']}"
        ).lower()

        assert "alice" in searchable_text    

def test_customer_pagination_rejects_invalid_page() -> None:
    response = client.get(
        "/api/v1/customers",
        params={
            "page": 0,
            "page_size": 10,
        },
    )

    assert response.status_code == 422


def test_customer_pagination_rejects_invalid_page_size() -> None:
    response = client.get(
        "/api/v1/customers",
        params={
            "page": 1,
            "page_size": 0,
        },
    )

    assert response.status_code == 422


def test_customer_pagination_rejects_negative_page_size() -> None:
    response = client.get(
        "/api/v1/customers",
        params={
            "page": 1,
            "page_size": -10,
        },
    )

    assert response.status_code == 422        