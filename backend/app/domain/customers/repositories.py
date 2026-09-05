from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.customers.entities import Customer


class CustomerRepository(ABC):

    @abstractmethod
    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Customer]:
        pass

    @abstractmethod
    async def add(self, customer: Customer) -> Customer:
        pass