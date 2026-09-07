from decimal import Decimal

from app.application.scoring.deterministic_customer_predictor import (
    DeterministicCustomerPredictor,
)
from app.domain.scoring.customer_features import CustomerFeatures


def test_predicts_zero_churn_for_active_high_value_customer() -> None:
    features = CustomerFeatures(
        transaction_count=10,
        total_transaction_value=Decimal("5000"),
        average_transaction_value=Decimal("500"),
        days_since_last_transaction=5,
    )

    predictor = DeterministicCustomerPredictor()

    prediction = predictor.predict(features)

    assert prediction.churn_probability == Decimal("0")


def test_predicts_high_churn_for_inactive_customer() -> None:
    features = CustomerFeatures(
        transaction_count=1,
        total_transaction_value=Decimal("20"),
        average_transaction_value=Decimal("20"),
        days_since_last_transaction=100,
    )

    predictor = DeterministicCustomerPredictor()

    prediction = predictor.predict(features)

    assert prediction.churn_probability == Decimal("0.80")


def test_prediction_probability_is_capped_at_one() -> None:
    features = CustomerFeatures(
        transaction_count=0,
        total_transaction_value=Decimal("0"),
        average_transaction_value=Decimal("0"),
        days_since_last_transaction=365,
    )

    predictor = DeterministicCustomerPredictor()

    prediction = predictor.predict(features)

    assert prediction.churn_probability == Decimal("0.80")