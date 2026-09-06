from uuid import uuid4

import pytest

from app.application.common.background_worker import BackgroundWorker
from app.application.scoring.customer_scoring_scheduler import (
    CustomerScoringScheduler,
)


class FakeScoringService:

    def __init__(self):
        self.customer_ids = []

    async def calculate_score(self, customer_id):
        self.customer_ids.append(customer_id)


@pytest.mark.asyncio
async def test_scheduler_enqueues_customer_scoring_job() -> None:
    worker = BackgroundWorker()
    scoring_service = FakeScoringService()

    scheduler = CustomerScoringScheduler(
        worker=worker,
        scoring_service=scoring_service,
    )

    customer_id = uuid4()

    await worker.start()

    await scheduler.schedule(customer_id)

    await worker._queue.join()

    await worker.stop()

    assert scoring_service.customer_ids == [customer_id]