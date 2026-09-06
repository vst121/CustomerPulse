from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class CustomerScore:
    customer_id: UUID
    score: Decimal