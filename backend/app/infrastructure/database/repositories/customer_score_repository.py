from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.scoring.entities import CustomerScore
from app.domain.scoring.repositories import CustomerScoreRepository
from app.infrastructure.database.models import CustomerScoreModel


class PostgresCustomerScoreRepository(CustomerScoreRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> CustomerScore | None:
        result = await self._session.execute(
            select(CustomerScoreModel).where(
                CustomerScoreModel.customer_id == customer_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def add(
        self,
        customer_score: CustomerScore,
    ) -> CustomerScore:
        model = CustomerScoreModel(
            customer_id=customer_score.customer_id,
            score=customer_score.score,
        )

        self._session.add(model)

        await self._session.flush()

        return self._to_domain(model)

    async def update(
        self,
        customer_score: CustomerScore,
    ) -> CustomerScore:
        result = await self._session.execute(
            select(CustomerScoreModel).where(
                CustomerScoreModel.customer_id
                == customer_score.customer_id
            )
        )

        model = result.scalar_one()

        model.score = customer_score.score

        await self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: CustomerScoreModel,
    ) -> CustomerScore:
        return CustomerScore(
            customer_id=model.customer_id,
            score=model.score,
        )