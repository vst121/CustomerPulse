from uuid import uuid4

import pytest

from app.application.common.background_worker import BackgroundWorker
from app.application.scoring.customer_scoring_scheduler import (
    CustomerScoringScheduler,
)


@pytest.mark.asyncio
async def test_scheduler_enqueues_customer_scoring_job():
    worker = BackgroundWorker()

    scheduler = CustomerScoringScheduler(
        worker=worker,
    )

    customer_id = uuid4()

    await worker.start()

    await scheduler.schedule(customer_id)

    await worker._queue.join()

    await worker.stop()