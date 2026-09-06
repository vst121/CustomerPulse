from uuid import UUID, uuid4

from app.application.common.unit_of_work import UnitOfWork
from app.domain.customers.entities import LifecycleStage
from app.domain.recommendations.entities import (
    Recommendation,
    RecommendationType,
)


class RecommendationService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def generate_recommendation(
        self,
        customer_id: UUID,
    ) -> Recommendation:

        async with self.uow:

            customer = await self.uow.customers.get_by_id(
                customer_id
            )

            if customer is None:
                raise ValueError(
                    f"Customer '{customer_id}' was not found."
                )

            customer_score = (
                await self.uow.customer_scores.get_by_customer_id(
                    customer_id
                )
            )

            score = (
                customer_score.score
                if customer_score is not None
                else 0
            )

            recommendation_type, reason = (
                self._determine_recommendation(
                    lifecycle_stage=customer.lifecycle_stage,
                    score=score,
                )
            )

            recommendation = Recommendation(
                id=uuid4(),
                customer_id=customer_id,
                type=recommendation_type,
                reason=reason,
            )

            recommendation = (
                await self.uow.recommendations.add(
                    recommendation
                )
            )

            await self.uow.commit()

            return recommendation

    @staticmethod
    def _determine_recommendation(
        lifecycle_stage: LifecycleStage,
        score,
    ) -> tuple[RecommendationType, str]:

        if lifecycle_stage == LifecycleStage.WIN_BACK:
            return (
                RecommendationType.REACTIVATION,
                "Customer is in the WIN_BACK lifecycle stage.",
            )

        if score >= 80:
            return (
                RecommendationType.LOYALTY_REWARD,
                "Customer has a high value score.",
            )

        if lifecycle_stage == LifecycleStage.RETENTION:
            return (
                RecommendationType.RETENTION_OFFER,
                "Customer is in the RETENTION lifecycle stage.",
            )

        if score >= 60:
            return (
                RecommendationType.UPSELL,
                "Customer has a strong value score.",
            )

        if score >= 40:
            return (
                RecommendationType.CROSS_SELL,
                "Customer has potential for additional products.",
            )

        return (
            RecommendationType.NO_ACTION,
            "No immediate action is recommended.",
        )