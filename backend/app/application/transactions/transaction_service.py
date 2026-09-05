from uuid import UUID, uuid4

from app.domain.transactions.entities import Transaction
from app.domain.transactions.repositories import TransactionRepository


class TransactionService:

    def __init__(
        self,
        repository: TransactionRepository,
    ):
        self._repository = repository

    async def create_transaction(
        self,
        customer_id: UUID,
        amount,
        currency: str,
        category,
        status,
        timestamp,
    ) -> Transaction:

        transaction = Transaction(
            id=uuid4(),
            customer_id=customer_id,
            amount=amount,
            currency=currency.upper(),
            category=category,
            status=status,
            timestamp=timestamp,
        )

        return await self._repository.add(transaction)

    async def get_transaction(
        self,
        transaction_id: UUID,
    ) -> Transaction | None:

        return await self._repository.get_by_id(
            transaction_id
        )

    async def get_customer_transactions(
        self,
        customer_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[Transaction], int]:

        return await self._repository.get_by_customer_id(
            customer_id=customer_id,
            page=page,
            page_size=page_size,
        )