from datetime import datetime, timezone
from uuid import UUID

from app.domain.customers.entities import (
    Customer,
    LifecycleStage,
)
from app.domain.customers.repositories import CustomerRepository


class CustomerAlreadyExistsError(Exception):
    pass


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

        if await self._repository.exists_by_email(email):
            raise CustomerAlreadyExistsError(
                f"Customer with email '{email}' already exists."
            )

        customer = Customer(
            id=UUID(int=0),
            first_name=first_name,
            last_name=last_name,
            email=email,
            lifecycle_stage=LifecycleStage.ACQUISITION,
            created_at=datetime.now(timezone.utc),
        )

        return await self._repository.add(customer)

    async def get_customer(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        return await self._repository.get_by_id(customer_id)

    async def get_customers(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        lifecycle_stage: LifecycleStage | None = None,
    ) -> tuple[list[Customer], int]:

        return await self._repository.get_all(
            page=page,
            page_size=page_size,
            search=search,
            lifecycle_stage=lifecycle_stage,
        )