from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.transactions.entities import (
    TransactionCategory,
    TransactionStatus,
)


class CreateTransactionRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    currency: str = Field(
        min_length=3,
        max_length=3,
    )
    category: TransactionCategory
    status: TransactionStatus = TransactionStatus.COMPLETED
    timestamp: datetime


class TransactionResponse(BaseModel):
    id: UUID
    customer_id: UUID
    amount: Decimal
    currency: str
    category: TransactionCategory
    status: TransactionStatus
    timestamp: datetime


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    page: int
    page_size: int
    total: int