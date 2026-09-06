import uuid
from uuid import UUID

import pytest

from app.domain.customers.entities import Customer
from app.application.customers.customer_service import (
    CustomerService,
)


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

    async def exists(
        self,
        customer_id: UUID,
    ) -> bool:
        return any(
            customer.id == customer_id
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


class FakeUnitOfWork:

    def __init__(
        self,
        repository: FakeCustomerRepository,
    ):
        self.customers = repository
        self.commit_count = 0
        self.rollback_count = 0

    async def commit(self) -> None:
        self.commit_count += 1

    async def rollback(self) -> None:
        self.rollback_count += 1


@pytest.mark.anyio
async def test_create_customer():

    repository = FakeCustomerRepository()

    uow = FakeUnitOfWork(repository)

    service = CustomerService(
        customer_repository=repository,
        uow=uow,
    )

    random_email = (
        f"anna_{uuid.uuid4().hex[:8]}@example.com"
    )

    customer = await service.create_customer(
        first_name="Anna",
        last_name="Müller",
        email=random_email,
    )

    assert customer.first_name == "Anna"

    assert customer.lifecycle_stage.value == "ACQUISITION"

    assert uow.commit_count == 1