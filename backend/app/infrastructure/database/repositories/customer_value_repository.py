from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.value.entities import CustomerValue
from app.domain.value.repositories import CustomerValueRepository
from app.infrastructure.database.models import CustomerValueModel


class PostgresCustomerValueRepository(
    CustomerValueRepository
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> CustomerValue | None:

        result = await self._session.execute(
            select(CustomerValueModel).where(
                CustomerValueModel.customer_id == customer_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def add(
        self,
        customer_value: CustomerValue,
    ) -> CustomerValue:

        model = CustomerValueModel(
            customer_id=customer_value.customer_id,
            total_spend=customer_value.total_spend,
            transaction_count=customer_value.transaction_count,
        )

        self._session.add(model)

        await self._session.flush()

        return self._to_domain(model)

    async def update(
        self,
        customer_value: CustomerValue,
    ) -> CustomerValue:

        result = await self._session.execute(
            select(CustomerValueModel).where(
                CustomerValueModel.customer_id
                == customer_value.customer_id
            )
        )

        model = result.scalar_one()

        model.total_spend = customer_value.total_spend
        model.transaction_count = (
            customer_value.transaction_count
        )

        await self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: CustomerValueModel,
    ) -> CustomerValue:

        return CustomerValue(
            customer_id=model.customer_id,
            total_spend=model.total_spend,
            transaction_count=model.transaction_count,
        )