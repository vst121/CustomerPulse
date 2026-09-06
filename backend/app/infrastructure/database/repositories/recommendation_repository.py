from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.recommendations.entities import (
    Recommendation,
    RecommendationType,
)
from app.domain.recommendations.repositories import (
    RecommendationRepository,
)
from app.infrastructure.database.models import RecommendationModel


class PostgresRecommendationRepository(
    RecommendationRepository
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> list[Recommendation]:

        result = await self._session.execute(
            select(RecommendationModel)
            .where(
                RecommendationModel.customer_id == customer_id
            )
            .order_by(
                RecommendationModel.id
            )
        )

        models = result.scalars().all()

        return [
            self._to_domain(model)
            for model in models
        ]

    async def add(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:

        model = RecommendationModel(
            id=recommendation.id,
            customer_id=recommendation.customer_id,
            type=recommendation.type.value,
            reason=recommendation.reason,
        )

        self._session.add(model)

        await self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: RecommendationModel,
    ) -> Recommendation:

        return Recommendation(
            id=model.id,
            customer_id=model.customer_id,
            type=RecommendationType(model.type),
            reason=model.reason,
        )