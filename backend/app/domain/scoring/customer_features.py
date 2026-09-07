from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CustomerFeatures:
    transaction_count: int
    total_transaction_value: Decimal
    average_transaction_value: Decimal
    days_since_last_transaction: int