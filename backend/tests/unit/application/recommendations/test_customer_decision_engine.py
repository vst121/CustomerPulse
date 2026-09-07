from decimal import Decimal

from app.application.recommendations.customer_decision_engine import (
    CustomerDecisionEngine,
)
from app.domain.recommendations.customer_decision import (
    CustomerDecisionType,
)
from app.domain.scoring.customer_prediction import CustomerPrediction


def test_high_churn_probability_produces_retention_decision() -> None:
    prediction = CustomerPrediction(
        churn_probability=Decimal("0.80"),
    )

    engine = CustomerDecisionEngine()

    decision = engine.decide(prediction)

    assert decision.decision_type == CustomerDecisionType.RETENTION
    assert decision.priority == 1


def test_medium_churn_probability_produces_engagement_decision() -> None:
    prediction = CustomerPrediction(
        churn_probability=Decimal("0.50"),
    )

    engine = CustomerDecisionEngine()

    decision = engine.decide(prediction)

    assert decision.decision_type == CustomerDecisionType.ENGAGEMENT
    assert decision.priority == 2


def test_low_churn_probability_produces_growth_decision() -> None:
    prediction = CustomerPrediction(
        churn_probability=Decimal("0.25"),
    )

    engine = CustomerDecisionEngine()

    decision = engine.decide(prediction)

    assert decision.decision_type == CustomerDecisionType.GROWTH
    assert decision.priority == 3


def test_very_low_churn_probability_produces_no_action() -> None:
    prediction = CustomerPrediction(
        churn_probability=Decimal("0.10"),
    )

    engine = CustomerDecisionEngine()

    decision = engine.decide(prediction)

    assert decision.decision_type == CustomerDecisionType.NO_ACTION
    assert decision.priority == 4