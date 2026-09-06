from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.application.exceptions import CustomerNotFoundError
from app.domain.customers.repositories import CustomerRepository
from app.domain.transactions.entities import (
    Transaction,
    TransactionCategory,
    TransactionStatus,
)
from app.domain.transactions.repositories import TransactionRepository


class TransactionService:

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        customer_repository: CustomerRepository,
    ):
        self.transaction_repository = transaction_repository
        self.customer_repository = customer_repository

    async def create_transaction(
        self,
        customer_id: UUID,
        idempotency_key: str,
        amount: Decimal,
        currency: str,
        category: TransactionCategory,
        status: TransactionStatus,
        timestamp: datetime,
    ) -> Transaction:

        customer_exists = await self.customer_repository.exists(
            customer_id
        )

        if not customer_exists:
            raise CustomerNotFoundError(customer_id)

        existing = await (
            self.transaction_repository
            .get_by_idempotency_key(
                customer_id,
                idempotency_key,
            )
        )

        if existing is not None:
            return existing

        transaction = Transaction(
            id=uuid4(),
            customer_id=customer_id,
            idempotency_key=idempotency_key,
            amount=amount,
            currency=currency.upper(),
            category=category,
            status=status,
            timestamp=timestamp,
        )

        return await self.transaction_repository.add(transaction)

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