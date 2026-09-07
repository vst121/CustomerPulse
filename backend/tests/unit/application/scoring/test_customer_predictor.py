import inspect

from app.application.scoring.customer_predictor import CustomerPredictor


def test_customer_predictor_is_abstract() -> None:
    assert inspect.isabstract(CustomerPredictor)