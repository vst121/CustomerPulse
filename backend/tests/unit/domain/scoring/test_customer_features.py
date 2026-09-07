from decimal import Decimal

from app.domain.scoring.customer_features import (
    CustomerFeatures,
)


def test_customer_features_are_immutable() -> None:
    features = CustomerFeatures(
        transaction_count=42,
        total_transaction_value=Decimal("8420"),
        average_transaction_value=Decimal("200"),
        days_since_last_transaction=34,
    )

    assert features.transaction_count == 42
    assert features.total_transaction_value == Decimal("8420")
    assert features.average_transaction_value == Decimal("200")
    assert features.days_since_last_transaction == 34