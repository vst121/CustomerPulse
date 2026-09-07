from app.domain.recommendations.customer_decision import (
    CustomerDecision,
    CustomerDecisionType,
)
from app.domain.recommendations.next_best_action import (
    NextBestAction,
    NextBestActionType,
)


class NextBestActionService:
    def determine(
        self,
        decision: CustomerDecision,
    ) -> NextBestAction:
        if decision.decision_type == CustomerDecisionType.RETENTION:
            return NextBestAction(
                action_type=NextBestActionType.RETENTION_OFFER,
                priority=decision.priority,
                reason="Customer has a high predicted churn risk.",
            )

        if decision.decision_type == CustomerDecisionType.ENGAGEMENT:
            return NextBestAction(
                action_type=NextBestActionType.ENGAGEMENT_CAMPAIGN,
                priority=decision.priority,
                reason="Customer shows an elevated churn risk.",
            )

        if decision.decision_type == CustomerDecisionType.GROWTH:
            return NextBestAction(
                action_type=NextBestActionType.GROWTH_OFFER,
                priority=decision.priority,
                reason="Customer has low churn risk and may be suitable for growth.",
            )

        return NextBestAction(
            action_type=NextBestActionType.NO_ACTION,
            priority=decision.priority,
            reason="Customer does not currently require an intervention.",
        )