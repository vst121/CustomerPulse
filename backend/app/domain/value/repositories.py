from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.value.entities import CustomerValue


class CustomerValueRepository(ABC):

    @abstractmethod
    async def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> CustomerValue | None:
        ...

    @abstractmethod
    async def add(
        self,
        customer_value: CustomerValue,
    ) -> CustomerValue:
        ...

    @abstractmethod
    async def update(
        self,
        customer_value: CustomerValue,
    ) -> CustomerValue:
        ...