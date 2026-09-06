import asyncio
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import select

from app.domain.transactions.entities import (
    TransactionCategory,
    TransactionStatus,
)
from app.infrastructure.database.database import (
    AsyncSessionLocal,
)
from app.infrastructure.database.models import TransactionModel
from app.infrastructure.database.repositories.transaction_repository import (
    PostgresTransactionRepository,
)


async def create_transaction(
    customer_id,
    idempotency_key: str,
):
    async with AsyncSessionLocal() as session:

        repository = PostgresTransactionRepository(session)

        transaction = TransactionModel(
            id=uuid4(),
            customer_id=customer_id,
            amount=Decimal("100.00"),
            currency="EUR",
            category=TransactionCategory.GROCERIES.value,
            status=TransactionStatus.COMPLETED.value,
            timestamp=datetime.now(timezone.utc),
            idempotency_key=idempotency_key,
        )

        session.add(transaction)

        try:
            await session.commit()

        except Exception:
            await session.rollback()

            existing = await session.execute(
                select(TransactionModel).where(
                    TransactionModel.customer_id == customer_id,
                    TransactionModel.idempotency_key
                    == idempotency_key,
                )
            )

            return existing.scalar_one()

        await session.refresh(transaction)

        return transaction