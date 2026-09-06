from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.transactions.entities import (
    TransactionCategory,
    TransactionStatus,
)
from app.infrastructure.database.database import (
    AsyncSessionLocal,
)
from app.infrastructure.database.models import TransactionModel
from app.infrastructure.database.unit_of_work import (
    PostgresUnitOfWork,
)
from backend.app.application.transactions.transaction_service import TransactionService


async def create_transaction(
    customer_id: UUID,
    idempotency_key: str,
):
    async with AsyncSessionLocal() as session:

        uow = PostgresUnitOfWork(session)

        service = TransactionService(
            uow=uow,
        )

        return await service.create_transaction(
            customer_id=customer_id,
            amount=Decimal("100.00"),
            currency="EUR",
            category=TransactionCategory.GROCERIES,
            status=TransactionStatus.COMPLETED,
            timestamp=datetime.now(timezone.utc),
            idempotency_key=idempotency_key,
        )