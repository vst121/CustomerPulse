from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from app.application.common.unit_of_work import UnitOfWork
from app.application.recommendations.customer_decision_engine import (
    CustomerDecisionEngine,
)
from app.application.recommendations.next_best_action_service import (
    NextBestActionService,
)
from app.application.scoring.customer_feature_extractor import (
    CustomerFeatureExtractor,
)
from app.application.scoring.customer_intelligence_service import (
    CustomerIntelligenceService,
)
from app.application.scoring.customer_predictor import CustomerPredictor
from app.domain.recommendations.customer_decision import (
    CustomerDecision,
    CustomerDecisionType,
)
from app.domain.recommendations.next_best_action import (
    NextBestAction,
    NextBestActionType,
)
from app.domain.scoring.customer_features import CustomerFeatures
from app.domain.scoring.customer_prediction import CustomerPrediction


@pytest.mark.asyncio
async def test_customer_intelligence_service_orchestrates_pipeline() -> None:
    customer_id = UUID("11111111-1111-1111-1111-111111111111")

    transactions = [
        Mock()
    ]

    expected_features = CustomerFeatures(
        transaction_count=1,
        total_transaction_value=Decimal("100"),
        average_transaction_value=Decimal("100"),
        days_since_last_transaction=10,
    )

    expected_prediction = CustomerPrediction(
        churn_probability=Decimal("0.20"),
    )

    expected_action = NextBestAction(
        action_type=NextBestActionType.GROWTH_OFFER,
        priority=3,
        reason="Customer has low churn risk and may be suitable for growth.",
    )

    uow = Mock(spec=UnitOfWork)

    uow.customers = Mock()
    uow.customers.get_by_id = AsyncMock(
        return_value=Mock()
    )

    uow.transactions = Mock()
    uow.transactions.get_all_by_customer_id = AsyncMock(
        return_value=transactions
    )

    feature_extractor = Mock(spec=CustomerFeatureExtractor)
    feature_extractor.extract.return_value = expected_features

    predictor = Mock(spec=CustomerPredictor)
    predictor.predict.return_value = expected_prediction

    decision_engine = Mock(spec=CustomerDecisionEngine)
    decision = CustomerDecision(
        decision_type=CustomerDecisionType.GROWTH,
        priority=3,
    )
    decision_engine.decide.return_value = decision

    action_service = Mock(spec=NextBestActionService)
    action_service.determine.return_value = expected_action

    service = CustomerIntelligenceService(
        uow=uow,
        feature_extractor=feature_extractor,
        predictor=predictor,
        decision_engine=decision_engine,
        action_service=action_service,
    )

    result = await service.analyze(customer_id)

    uow.customers.get_by_id.assert_awaited_once_with(
        customer_id
    )

    uow.transactions.get_all_by_customer_id.assert_awaited_once_with(
        customer_id
    )

    feature_extractor.extract.assert_called_once_with(
        transactions
    )

    predictor.predict.assert_called_once_with(
        expected_features
    )

    decision_engine.decide.assert_called_once_with(
        expected_prediction
    )

    action_service.determine.assert_called_once_with(
        decision
    )

    assert result.features == expected_features
    assert result.prediction == expected_prediction
    assert result.action == expected_action
