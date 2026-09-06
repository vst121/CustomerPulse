from typing import Any
from uuid import UUID

from app.application.common.background_job import BackgroundJob
from app.application.scoring.customer_scoring_service import (
    CustomerScoringService,
)


class CustomerScoringJob(BackgroundJob):

    def __init__(
        self,
        scoring_service: CustomerScoringService,
    ):
        self.scoring_service = scoring_service

    async def execute(
        self,
        payload: dict[str, Any],
    ) -> None:
        customer_id = UUID(payload["customer_id"])

        await self.scoring_service.calculate_score(
            customer_id
        )