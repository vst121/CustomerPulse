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
from app.application.scoring.customer_predictor import CustomerPredictor
from app.domain.recommendations.next_best_action import NextBestAction
from app.domain.scoring.customer_features import CustomerFeatures
from app.domain.scoring.customer_prediction import CustomerPrediction
from uuid import UUID


class CustomerIntelligenceResult:
    def __init__(
        self,
        features: CustomerFeatures,
        prediction: CustomerPrediction,
        action: NextBestAction,
    ) -> None:
        self.features = features
        self.prediction = prediction
        self.action = action


class CustomerIntelligenceService:

    def __init__(
        self,
        uow: UnitOfWork,
        feature_extractor: CustomerFeatureExtractor,
        predictor: CustomerPredictor,
        decision_engine: CustomerDecisionEngine,
        action_service: NextBestActionService,
    ) -> None:
        self._uow = uow
        self._feature_extractor = feature_extractor
        self._predictor = predictor
        self._decision_engine = decision_engine
        self._action_service = action_service

    async def analyze(
        self,
        customer_id: UUID,
    ) -> CustomerIntelligenceResult:

        customer = await self._uow.customers.get_by_id(
            customer_id
        )

        if customer is None:
            raise ValueError("Customer not found.")

        transactions = (
            await self._uow.transactions.get_all_by_customer_id(
                customer_id
            )
        )

        features = self._feature_extractor.extract(
            transactions
        )

        prediction = self._predictor.predict(
            features
        )

        decision = self._decision_engine.decide(
            prediction
        )

        action = self._action_service.determine(
            decision
        )

        return CustomerIntelligenceResult(
            features=features,
            prediction=prediction,
            action=action,
        )