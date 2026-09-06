from uuid import UUID

from app.application.common.background_worker import BackgroundWorker
from app.application.scoring.customer_scoring_job import CustomerScoringJob


class CustomerScoringScheduler:
    def __init__(self, worker: BackgroundWorker):
        self.worker = worker

    async def schedule(self, customer_id: UUID) -> None:
        job = CustomerScoringJob()

        await self.worker.enqueue(
            job,
            {"customer_id": str(customer_id)},
        )