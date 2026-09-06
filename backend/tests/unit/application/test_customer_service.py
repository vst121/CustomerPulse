import uuid
from uuid import UUID

import pytest

from app.domain.customers.entities import Customer
from app.application.customers.customer_service import (
    CustomerService,
)
from app.application.common.unit_of_work import UnitOfWork
from backend.tests.unit.application.test_unit_of_work import FakeUnitOfWork

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

@pytest.mark.anyio
async def test_create_customer():

    customer_repository = FakeCustomerRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=None,
    )

    service = CustomerService(
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