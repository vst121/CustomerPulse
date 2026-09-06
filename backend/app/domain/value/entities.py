from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class CustomerValue:
    customer_id: UUID
    total_spend: Decimal
    transaction_count: int