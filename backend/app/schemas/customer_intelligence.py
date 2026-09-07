from decimal import Decimal
from pydantic import BaseModel


class CustomerIntelligenceFeaturesResponse(BaseModel):
    transaction_count: int
    total_transaction_value: Decimal
    average_transaction_value: Decimal
    days_since_last_transaction: int


class CustomerIntelligencePredictionResponse(BaseModel):
    churn_probability: Decimal


class CustomerIntelligenceActionResponse(BaseModel):
    action_type: str
    priority: int
    reason: str


class CustomerIntelligenceResponse(BaseModel):
    features: CustomerIntelligenceFeaturesResponse
    prediction: CustomerIntelligencePredictionResponse
    action: CustomerIntelligenceActionResponse