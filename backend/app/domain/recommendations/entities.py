from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class RecommendationType(StrEnum):
    RETENTION_OFFER = "RETENTION_OFFER"
    UPSELL = "UPSELL"
    CROSS_SELL = "CROSS_SELL"
    REACTIVATION = "REACTIVATION"
    LOYALTY_REWARD = "LOYALTY_REWARD"
    NO_ACTION = "NO_ACTION"


@dataclass
class Recommendation:
    id: UUID
    customer_id: UUID
    type: RecommendationType
    reason: str