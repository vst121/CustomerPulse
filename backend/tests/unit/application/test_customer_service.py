
from uuid import UUID

from app.domain.customers.entities import Customer


class FakeCustomerRepository:

    def __init__(self):
        self.customers: list[Customer] = []

    async def exists_by_email(
        self,
        email: str,
    ) -> bool:

        return any(
            customer.email == email
            for customer in self.customers
        )

    async def add(
        self,
        customer: Customer,
    ) -> Customer:

        self.customers.append(customer)

        return customer

    async def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        return next(
            (
                customer
                for customer in self.customers
                if customer.id == customer_id
            ),
            None,
        )

import pytest

from app.application.customers.customer_service import (
    CustomerAlreadyExistsError,
    CustomerService,
)


@pytest.mark.anyio
async def test_create_customer():

    repository = FakeCustomerRepository()
    service = CustomerService(repository)

    customer = await service.create_customer(
        first_name="Anna",
        last_name="Müller",
        email="anna@example.com",
    )

    assert customer.first_name == "Anna"
    assert customer.lifecycle_stage.value == "ACQUISITION"