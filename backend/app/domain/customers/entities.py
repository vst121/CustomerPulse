from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class LifecycleStage(StrEnum):
    ACQUISITION = "ACQUISITION"
    ONBOARDING = "ONBOARDING"
    ACTIVATION = "ACTIVATION"
    ENGAGEMENT = "ENGAGEMENT"
    GROWTH = "GROWTH"
    RETENTION = "RETENTION"
    WIN_BACK = "WIN_BACK"


@dataclass
class Customer:
    id: UUID
    first_name: str
    last_name: str
    email: str
    lifecycle_stage: LifecycleStage
    created_at: datetime