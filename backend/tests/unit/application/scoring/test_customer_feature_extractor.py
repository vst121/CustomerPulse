from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from app.application.scoring.customer_feature_extractor import (
    CustomerFeatureExtractor,
)
from app.domain.transactions.entities import (
    Transaction,
    TransactionCategory,
    TransactionStatus,
)


def create_transaction(
    amount: str,
    timestamp: datetime,
    status: TransactionStatus = TransactionStatus.COMPLETED,
) -> Transaction:
    return Transaction(
        id=uuid4(),
        customer_id=uuid4(),
        idempotency_key=str(uuid4()),
        amount=Decimal(amount),
        currency="EUR",
        category=TransactionCategory.SHOPPING,
        status=status,
        timestamp=timestamp,
    )


def test_extracts_customer_features() -> None:
    now = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)

    transactions = [
        create_transaction(
            "100",
            datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
        ),
        create_transaction(
            "200",
            datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc),
        ),
    ]

    extractor = CustomerFeatureExtractor()

    features = extractor.extract(
        transactions,
        now=now,
    )

    assert features.transaction_count == 2
    assert features.total_transaction_value == Decimal("300")
    assert features.average_transaction_value == Decimal("150")
    assert features.days_since_last_transaction == 2


def test_ignores_non_completed_transactions() -> None:
    now = datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)

    transactions = [
        create_transaction(
            "100",
            datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc),
        ),
        create_transaction(
            "500",
            datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc),
            status=TransactionStatus.FAILED,
        ),
    ]

    extractor = CustomerFeatureExtractor()

    features = extractor.extract(
        transactions,
        now=now,
    )

    assert features.transaction_count == 1
    assert features.total_transaction_value == Decimal("100")
    assert features.average_transaction_value == Decimal("100")
    assert features.days_since_last_transaction == 6


def test_returns_zero_features_without_transactions() -> None:
    extractor = CustomerFeatureExtractor()

    features = extractor.extract([])

    assert features.transaction_count == 0
    assert features.total_transaction_value == Decimal("0")
    assert features.average_transaction_value == Decimal("0")
    assert features.days_since_last_transaction == 0