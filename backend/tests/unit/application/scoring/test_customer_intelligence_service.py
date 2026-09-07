from decimal import Decimal
from unittest.mock import Mock

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
from app.application.scoring.deterministic_customer_predictor import (
    DeterministicCustomerPredictor,
)
from app.domain.recommendations.next_best_action import (
    NextBestActionType,
)
from app.domain.scoring.customer_features import CustomerFeatures
from app.domain.scoring.customer_prediction import CustomerPrediction


def test_customer_intelligence_service_orchestrates_prediction_pipeline() -> None:
    feature_extractor = Mock(spec=CustomerFeatureExtractor)
    predictor = Mock(spec=DeterministicCustomerPredictor)
    decision_engine = Mock(spec=CustomerDecisionEngine)
    action_service = Mock(spec=NextBestActionService)

    features = CustomerFeatures(
        transaction_count=5,
        total_transaction_value=Decimal("500"),
        average_transaction_value=Decimal("100"),
        days_since_last_transaction=10,
    )

    prediction = CustomerPrediction(
        churn_probability=Decimal("0.10"),
    )

    decision = Mock()

    action = Mock()
    action.action_type = NextBestActionType.NO_ACTION

    feature_extractor.extract.return_value = features
    predictor.predict.return_value = prediction
    decision_engine.decide.return_value = decision
    action_service.determine.return_value = action

    service = CustomerIntelligenceService(
        feature_extractor=feature_extractor,
        predictor=predictor,
        decision_engine=decision_engine,
        action_service=action_service,
    )

    result = service.analyze([])

    assert result.features == features
    assert result.prediction == prediction
    assert result.action == action

    feature_extractor.extract.assert_called_once_with([])
    predictor.predict.assert_called_once_with(features)
    decision_engine.decide.assert_called_once_with(prediction)
    action_service.determine.assert_called_once_with(decision)