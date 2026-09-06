from abc import ABC, abstractmethod

from app.domain.customers.repositories import CustomerRepository
from app.domain.transactions.repositories import TransactionRepository


class UnitOfWork(ABC):

    customers: CustomerRepository
    transactions: TransactionRepository

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...