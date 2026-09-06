from abc import ABC, abstractmethod

from app.domain.customers.repositories import CustomerRepository
from app.domain.transactions.repositories import TransactionRepository


class UnitOfWork(ABC):

    customers: CustomerRepository
    transactions: TransactionRepository

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        if exc_type is not None:
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...