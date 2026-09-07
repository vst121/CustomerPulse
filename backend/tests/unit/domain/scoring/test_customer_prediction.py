from decimal import Decimal

import pytest

from app.domain.scoring.customer_prediction import (
    CustomerPrediction,
)


def test_customer_prediction_accepts_valid_probability() -> None:
    prediction = CustomerPrediction(
        churn_probability=Decimal("0.82")
    )

    assert prediction.churn_probability == Decimal("0.82")


def test_customer_prediction_accepts_zero() -> None:
    prediction = CustomerPrediction(
        churn_probability=Decimal("0")
    )

    assert prediction.churn_probability == Decimal("0")


def test_customer_prediction_accepts_one() -> None:
    prediction = CustomerPrediction(
        churn_probability=Decimal("1")
    )

    assert prediction.churn_probability == Decimal("1")


def test_customer_prediction_rejects_probability_above_one() -> None:
    with pytest.raises(ValueError):
        CustomerPrediction(
            churn_probability=Decimal("1.01")
        )


def test_customer_prediction_rejects_probability_below_zero() -> None:
    with pytest.raises(ValueError):
        CustomerPrediction(
            churn_probability=Decimal("-0.01")
        )