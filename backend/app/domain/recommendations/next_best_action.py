from dataclasses import dataclass
from enum import StrEnum


class NextBestActionType(StrEnum):
    RETENTION_OFFER = "RETENTION_OFFER"
    ENGAGEMENT_CAMPAIGN = "ENGAGEMENT_CAMPAIGN"
    GROWTH_OFFER = "GROWTH_OFFER"
    NO_ACTION = "NO_ACTION"


@dataclass(frozen=True)
class NextBestAction:
    action_type: NextBestActionType
    priority: int
    reason: str