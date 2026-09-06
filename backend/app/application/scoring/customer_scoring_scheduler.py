from uuid import UUID

from app.application.common.background_worker import BackgroundWorker
from app.application.scoring.customer_scoring_job import CustomerScoringJob
from app.application.scoring.customer_scoring_service import (
    CustomerScoringService,
)


class CustomerScoringScheduler:

    def __init__(
        self,
        worker: BackgroundWorker,
        scoring_service: CustomerScoringService,
    ):
        self.worker = worker
        self.scoring_service = scoring_service

    async def schedule(
        self,
        customer_id: UUID,
    ) -> None:
        job = CustomerScoringJob(
            scoring_service=self.scoring_service,
        )

        await self.worker.enqueue(
            job,
            {
                "customer_id": str(customer_id),
            },
        )