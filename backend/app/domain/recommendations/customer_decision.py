from dataclasses import dataclass
from enum import StrEnum


class CustomerDecisionType(StrEnum):
    RETENTION = "RETENTION"
    ENGAGEMENT = "ENGAGEMENT"
    GROWTH = "GROWTH"
    NO_ACTION = "NO_ACTION"


@dataclass(frozen=True)
class CustomerDecision:
    decision_type: CustomerDecisionType
    priority: int