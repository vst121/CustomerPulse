from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class TransactionStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class TransactionCategory(StrEnum):
    GROCERIES = "GROCERIES"
    RESTAURANT = "RESTAURANT"
    TRAVEL = "TRAVEL"
    SHOPPING = "SHOPPING"
    UTILITIES = "UTILITIES"
    ENTERTAINMENT = "ENTERTAINMENT"
    OTHER = "OTHER"


@dataclass
class Transaction:
    id: UUID
    customer_id: UUID
    amount: Decimal
    currency: str
    category: TransactionCategory
    status: TransactionStatus
    timestamp: datetime