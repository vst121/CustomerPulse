from abc import ABC, abstractmethod

from app.domain.customers.repositories import CustomerRepository
from app.domain.transactions.repositories import TransactionRepository
from app.domain.value.repositories import CustomerValueRepository
from app.domain.scoring.repositories import CustomerScoreRepository
    
class UnitOfWork(ABC):

    customers: CustomerRepository
    transactions: TransactionRepository
    customer_values: CustomerValueRepository
    customer_scores: CustomerScoreRepository

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