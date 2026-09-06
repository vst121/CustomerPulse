from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.customers.entities import (
    Customer,
    LifecycleStage,
)
from app.domain.customers.repositories import CustomerRepository
from app.application.common.unit_of_work import UnitOfWork

class CustomerAlreadyExistsError(Exception):
    pass


class CustomerService:

    def __init__(
        self,
        customer_repository: CustomerRepository,
        uow: UnitOfWork,
    ):
        self.customer_repository = customer_repository
        self.uow = uow

    async def create_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
    ) -> Customer:

        if await self.customer_repository.exists_by_email(email):
            raise CustomerAlreadyExistsError(
                f"Customer with email '{email}' already exists."
            )

        customer = Customer(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            lifecycle_stage=LifecycleStage.ACQUISITION,
            created_at=datetime.now(timezone.utc),
        )

        created_customer = await self.customer_repository.add(customer)
        await self.uow.commit()

        return created_customer

    async def get_customer(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        return await self.customer_repository.get_by_id(customer_id)

    async def get_customers(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        lifecycle_stage: LifecycleStage | None = None,
    ) -> tuple[list[Customer], int]:

        return await self.customer_repository.get_all(
            page=page,
            page_size=page_size,
            search=search,
            lifecycle_stage=lifecycle_stage,
        )