from datetime import datetime, timezone
from decimal import Decimal

from app.domain.scoring.customer_features import CustomerFeatures
from app.domain.transactions.entities import (
    Transaction,
    TransactionStatus,
)


class CustomerFeatureExtractor:
    def extract(
        self,
        transactions: list[Transaction],
        now: datetime | None = None,
    ) -> CustomerFeatures:
        completed_transactions = [
            transaction
            for transaction in transactions
            if transaction.status == TransactionStatus.COMPLETED
        ]

        if not completed_transactions:
            return CustomerFeatures(
                transaction_count=0,
                total_transaction_value=Decimal("0"),
                average_transaction_value=Decimal("0"),
                days_since_last_transaction=0,
            )

        total_transaction_value = sum(
            (
                transaction.amount
                for transaction in completed_transactions
            ),
            Decimal("0"),
        )

        transaction_count = len(completed_transactions)

        average_transaction_value = (
            total_transaction_value / transaction_count
        )

        latest_transaction = max(
            completed_transactions,
            key=lambda transaction: transaction.timestamp,
        )

        current_time = now or datetime.now(timezone.utc)

        days_since_last_transaction = (
            current_time - latest_transaction.timestamp
        ).days

        return CustomerFeatures(
            transaction_count=transaction_count,
            total_transaction_value=total_transaction_value,
            average_transaction_value=average_transaction_value,
            days_since_last_transaction=days_since_last_transaction,
        )