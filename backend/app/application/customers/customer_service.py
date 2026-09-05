from datetime import datetime, timezone
from uuid import uuid4

from app.domain.customers.entities import Customer
from app.domain.customers.repositories import CustomerRepository


class CustomerService:

    def __init__(
        self,
        repository: CustomerRepository,
    ):
        self._repository = repository

    async def create_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
    ) -> Customer:

        customer = Customer(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            lifecycle_stage="ACQUISITION",
            created_at=datetime.now(timezone.utc),
        )

        return await self._repository.add(customer)

    async def get_customer(
        self,
        customer_id,
    ) -> Customer | None:

        return await self._repository.get_by_id(customer_id)

    async def get_customers(self) -> list[Customer]:

        return await self._repository.get_all()