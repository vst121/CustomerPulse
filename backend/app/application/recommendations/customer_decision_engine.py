from decimal import Decimal

from app.domain.recommendations.customer_decision import (
    CustomerDecision,
    CustomerDecisionType,
)
from app.domain.scoring.customer_prediction import CustomerPrediction


class CustomerDecisionEngine:
    def decide(
        self,
        prediction: CustomerPrediction,
    ) -> CustomerDecision:
        churn_probability = prediction.churn_probability

        if churn_probability >= Decimal("0.70"):
            return CustomerDecision(
                decision_type=CustomerDecisionType.RETENTION,
                priority=1,
            )

        if churn_probability >= Decimal("0.40"):
            return CustomerDecision(
                decision_type=CustomerDecisionType.ENGAGEMENT,
                priority=2,
            )

        if churn_probability >= Decimal("0.20"):
            return CustomerDecision(
                decision_type=CustomerDecisionType.GROWTH,
                priority=3,
            )

        return CustomerDecision(
            decision_type=CustomerDecisionType.NO_ACTION,
            priority=4,
        )