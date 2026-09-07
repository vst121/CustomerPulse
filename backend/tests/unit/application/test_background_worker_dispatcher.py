import pytest

from app.application.common.background_job import BackgroundJob
from app.application.common.background_worker import BackgroundWorker
from app.application.common.background_worker_dispatcher import (
    BackgroundWorkerDispatcher,
)


class SuccessfulJob(BackgroundJob):
    def __init__(self) -> None:
        self.payload: dict | None = None

    async def execute(self, payload: dict) -> None:
        self.payload = payload


@pytest.mark.asyncio
async def test_dispatcher_dispatches_job_to_worker() -> None:
    worker = BackgroundWorker()

    dispatcher = BackgroundWorkerDispatcher(
        worker=worker,
    )

    job = SuccessfulJob()
    payload = {"customer_id": "123"}

    await worker.start()

    await dispatcher.dispatch(
        job,
        payload,
    )

    await worker._queue.join()

    assert job.payload == payload

    await worker.stop()