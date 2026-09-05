from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Customer:
    id: UUID
    first_name: str
    last_name: str
    email: str
    lifecycle_stage: str
    created_at: datetime