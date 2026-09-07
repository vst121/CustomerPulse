from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Customer360Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: Decimal
    currency: str
    category: str
    status: str
    timestamp: datetime


class Customer360Recommendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    type: str
    reason: str


class Customer360Value(BaseModel):
    total_spend: Decimal
    transaction_count: int


class Customer360Score(BaseModel):
    score: Decimal


class Customer360Response(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    lifecycle_stage: str
    created_at: datetime

    value: Customer360Value
    score: Customer360Score
    transactions: list[Customer360Transaction]
    recommendations: list[Customer360Recommendation]