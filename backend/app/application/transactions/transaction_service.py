from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.application.common.unit_of_work import UnitOfWork
from app.domain.transactions.entities import (
    Transaction,
    TransactionCategory,
    TransactionStatus,
)


class TransactionService:

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    async def create_transaction(
        self,
        customer_id: UUID,
        amount: Decimal,
        currency: str,
        category: TransactionCategory,
        status: TransactionStatus,
        timestamp: datetime,
        idempotency_key: str,
    ) -> Transaction:

        customer = await self.uow.customers.get_by_id(
            customer_id
        )

        if customer is None:
            raise ValueError(
                f"Customer '{customer_id}' was not found."
            )

        existing = (
            await self.uow.transactions.get_by_idempotency_key(
                customer_id=customer_id,
                idempotency_key=idempotency_key,
            )
        )

        if existing is not None:
            return existing

        transaction = Transaction(
            id=uuid4(),
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            category=category,
            status=status,
            timestamp=timestamp,
            idempotency_key=idempotency_key,
        )

        transaction = await self.uow.transactions.add(
            transaction
        )

        await self.uow.commit()

        return transaction
    
    async def get_transaction(
        self,
        transaction_id: UUID,
    ) -> Transaction | None:

        return await self.transaction_repository.get_by_id(
            transaction_id
        )

    async def get_customer_transactions(
        self,
        customer_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[Transaction], int]:

        return await self.transaction_repository.get_by_customer_id(
            customer_id=customer_id,
            page=page,
            page_size=page_size,
        )