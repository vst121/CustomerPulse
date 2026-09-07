from decimal import Decimal

from app.application.scoring.customer_predictor import CustomerPredictor
from app.domain.scoring.customer_features import CustomerFeatures
from app.domain.scoring.customer_prediction import CustomerPrediction


class DeterministicCustomerPredictor(CustomerPredictor):
    def predict(
        self,
        features: CustomerFeatures,
    ) -> CustomerPrediction:
        probability = Decimal("0")

        if features.days_since_last_transaction >= 90:
            probability += Decimal("0.50")
        elif features.days_since_last_transaction >= 60:
            probability += Decimal("0.35")
        elif features.days_since_last_transaction >= 30:
            probability += Decimal("0.20")

        if features.transaction_count <= 1:
            probability += Decimal("0.20")
        elif features.transaction_count <= 3:
            probability += Decimal("0.10")

        if features.average_transaction_value < Decimal("50"):
            probability += Decimal("0.10")

        probability = min(probability, Decimal("1"))

        return CustomerPrediction(
            churn_probability=probability,
        )