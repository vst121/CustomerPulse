from app.application.recommendations.next_best_action_service import (
    NextBestActionService,
)
from app.domain.recommendations.customer_decision import (
    CustomerDecision,
    CustomerDecisionType,
)
from app.domain.recommendations.next_best_action import (
    NextBestActionType,
)


def test_retention_decision_produces_retention_offer() -> None:
    decision = CustomerDecision(
        decision_type=CustomerDecisionType.RETENTION,
        priority=1,
    )

    service = NextBestActionService()

    action = service.determine(decision)

    assert action.action_type == NextBestActionType.RETENTION_OFFER
    assert action.priority == 1
    assert "churn" in action.reason.lower()


def test_engagement_decision_produces_engagement_campaign() -> None:
    decision = CustomerDecision(
        decision_type=CustomerDecisionType.ENGAGEMENT,
        priority=2,
    )

    service = NextBestActionService()

    action = service.determine(decision)

    assert action.action_type == NextBestActionType.ENGAGEMENT_CAMPAIGN
    assert action.priority == 2


def test_growth_decision_produces_growth_offer() -> None:
    decision = CustomerDecision(
        decision_type=CustomerDecisionType.GROWTH,
        priority=3,
    )

    service = NextBestActionService()

    action = service.determine(decision)

    assert action.action_type == NextBestActionType.GROWTH_OFFER
    assert action.priority == 3


def test_no_action_decision_produces_no_action() -> None:
    decision = CustomerDecision(
        decision_type=CustomerDecisionType.NO_ACTION,
        priority=4,
    )

    service = NextBestActionService()

    action = service.determine(decision)

    assert action.action_type == NextBestActionType.NO_ACTION
    assert action.priority == 4