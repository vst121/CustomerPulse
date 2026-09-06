import asyncio
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.application.transactions.transaction_service import (
    TransactionService,
)
from app.domain.transactions.entities import (
    TransactionCategory,
    TransactionStatus,
)
from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.models import (
    CustomerModel,
    TransactionModel,
)
from app.infrastructure.database.unit_of_work import (
    PostgresUnitOfWork,
)

async def get_test_customer_id() -> UUID:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(CustomerModel.id).limit(1)
        )

        customer_id = result.scalar_one_or_none()

        if customer_id is None:
            raise RuntimeError(
                "No customer exists for the concurrency test."
            )

        return customer_id


async def create_transaction(
    customer_id: UUID,
    idempotency_key: str,
):
    async with AsyncSessionLocal() as session:

        uow = PostgresUnitOfWork(session)

        service = TransactionService(
            uow=uow,
        )

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


@pytest.mark.asyncio
async def test_concurrent_idempotent_requests_create_one_transaction():
    customer_id = await get_test_customer_id()

    idempotency_key = (
        f"concurrent-test-{uuid4()}"
    )

    request_count = 10

    results = await asyncio.gather(
        *[
            create_transaction(
                customer_id=customer_id,
                idempotency_key=idempotency_key,
            )
            for _ in range(request_count)
        ]
    )

    assert len(results) == request_count

    transaction_ids = {
        transaction.id
        for transaction in results
    }

    assert len(transaction_ids) == 1

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(func.count(TransactionModel.id)).where(
                TransactionModel.customer_id == customer_id,
                TransactionModel.idempotency_key
                == idempotency_key,
            )
        )

        transaction_count = result.scalar_one()

    assert transaction_count == 1