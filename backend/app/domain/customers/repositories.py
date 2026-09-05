from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.customers.entities import Customer, LifecycleStage


class CustomerRepository(ABC):

    @abstractmethod
    async def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:
        pass

    @abstractmethod
    async def get_all(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        lifecycle_stage: LifecycleStage | None = None,
    ) -> tuple[list[Customer], int]:
        pass

    @abstractmethod
    async def add(
        self,
        customer: Customer,
    ) -> Customer:
        pass

    @abstractmethod
    async def exists_by_email(
        self,
        email: str,
    ) -> bool:
        pass

    @abstractmethod
    async def exists(
        self, 
        customer_id: UUID
    ) -> bool:
        ...