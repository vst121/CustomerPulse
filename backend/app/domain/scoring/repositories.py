from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.scoring.entities import CustomerScore


class CustomerScoreRepository(ABC):

    @abstractmethod
    async def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> CustomerScore | None:
        ...

    @abstractmethod
    async def add(
        self,
        customer_score: CustomerScore,
    ) -> CustomerScore:
        ...

    @abstractmethod
    async def update(
        self,
        customer_score: CustomerScore,
    ) -> CustomerScore:
        ...