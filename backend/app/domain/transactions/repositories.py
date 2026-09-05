from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.transactions.entities import Transaction


class TransactionRepository(ABC):

    @abstractmethod
    async def get_by_id(
        self,
        transaction_id: UUID,
    ) -> Transaction | None:
        pass

    @abstractmethod
    async def get_by_customer_id(
        self,
        customer_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[Transaction], int]:
        pass

    @abstractmethod
    async def add(
        self,
        transaction: Transaction,
    ) -> Transaction:
        pass