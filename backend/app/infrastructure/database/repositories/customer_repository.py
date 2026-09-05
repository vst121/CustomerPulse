from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customers.entities import Customer
from app.domain.customers.repositories import CustomerRepository
from app.infrastructure.database.models import CustomerModel


class PostgresCustomerRepository(CustomerRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        result = await self._session.execute(
            select(CustomerModel).where(
                CustomerModel.id == customer_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def get_all(self) -> list[Customer]:

        result = await self._session.execute(
            select(CustomerModel)
        )

        models = result.scalars().all()

        return [
            self._to_domain(model)
            for model in models
        ]

    async def add(
        self,
        customer: Customer,
    ) -> Customer:

        model = CustomerModel(
            id=customer.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            lifecycle_stage=customer.lifecycle_stage,
            created_at=customer.created_at,
        )

        self._session.add(model)

        await self._session.commit()
        await self._session.refresh(model)

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: CustomerModel,
    ) -> Customer:

        return Customer(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            lifecycle_stage=model.lifecycle_stage,
            created_at=model.created_at,
        )