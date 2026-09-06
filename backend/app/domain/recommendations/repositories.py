from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.recommendations.entities import Recommendation


class RecommendationRepository(ABC):

    @abstractmethod
    async def get_by_customer_id(
        self,
        customer_id: UUID,
    ) -> list[Recommendation]:
        ...

    @abstractmethod
    async def add(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:
        ...