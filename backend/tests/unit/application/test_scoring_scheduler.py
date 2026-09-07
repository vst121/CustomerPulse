from uuid import UUID

import pytest

from app.application.common.background_worker import BackgroundWorker
from app.application.common.background_worker_dispatcher import (
    BackgroundWorkerDispatcher,
)
from app.application.scoring.scoring_scheduler import (
    CustomerScoringScheduler,
)


@pytest.mark.asyncio
async def test_scheduler_dispatches_customer_scoring_job() -> None:
    worker = BackgroundWorker()

    dispatcher = BackgroundWorkerDispatcher(
        worker=worker,
    )

    scheduler = CustomerScoringScheduler(
        dispatcher=dispatcher,
    )

    customer_id = UUID(
        "11111111-1111-1111-1111-111111111111"
    )

    await worker.start()

    await scheduler.schedule(
        customer_id,
    )

    assert worker.queue_size == 1

    await worker.stop()