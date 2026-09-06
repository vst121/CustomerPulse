from typing import Any
from uuid import UUID

from app.application.common.background_job import BackgroundJob
from app.application.scoring.customer_scoring_service import (
    CustomerScoringService,
)
from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.unit_of_work import PostgresUnitOfWork


class CustomerScoringJob(BackgroundJob):
    async def execute(self, payload: dict[str, Any]) -> None:
        customer_id = UUID(payload["customer_id"])

        async with AsyncSessionLocal() as session:
            uow = PostgresUnitOfWork(session)
            scoring_service = CustomerScoringService(uow=uow)

            await scoring_service.calculate_score(customer_id)