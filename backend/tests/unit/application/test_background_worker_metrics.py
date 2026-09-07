import pytest

from app.application.common.background_job import BackgroundJob
from app.application.common.background_worker import BackgroundWorker
from backend.app.application.common.background_worker_options import BackgroundWorkerOptions


class SuccessfulJob(BackgroundJob):
    async def execute(self, payload: dict) -> None:
        return


class EventuallySuccessfulJob(BackgroundJob):
    def __init__(self) -> None:
        self.attempts = 0

    async def execute(self, payload: dict) -> None:
        self.attempts += 1

        if self.attempts < 2:
            raise RuntimeError("temporary failure")


class PermanentlyFailingJob(BackgroundJob):
    async def execute(self, payload: dict) -> None:
        raise RuntimeError("permanent failure")


@pytest.mark.asyncio
async def test_successful_job_updates_metrics() -> None:
    worker = BackgroundWorker()

    await worker.start()

    await worker.enqueue(
        SuccessfulJob(),
        {},
    )

    await worker._queue.join()

    metrics = worker.metrics

    assert metrics.jobs_started == 1
    assert metrics.jobs_completed == 1
    assert metrics.jobs_failed == 0
    assert metrics.jobs_retried == 0

    await worker.stop()


@pytest.mark.asyncio
async def test_retry_updates_retry_metrics() -> None:
    worker = BackgroundWorker(
        options=BackgroundWorkerOptions(
            max_retries=3,
            retry_delay=0,
        ),
    )

    job = EventuallySuccessfulJob()

    await worker.start()

    await worker.enqueue(
        job,
        {},
    )

    await worker._queue.join()

    metrics = worker.metrics

    assert metrics.jobs_started == 1
    assert metrics.jobs_completed == 1
    assert metrics.jobs_failed == 0
    assert metrics.jobs_retried == 1

    await worker.stop()


@pytest.mark.asyncio
async def test_permanent_failure_updates_failure_metrics() -> None:
    worker = BackgroundWorker(
        options=BackgroundWorkerOptions(
            max_retries=3,
            retry_delay=0,
        ),
    )

    await worker.start()

    await worker.enqueue(
        PermanentlyFailingJob(),
        {},
    )

    await worker._queue.join()

    metrics = worker.metrics

    assert metrics.jobs_started == 1
    assert metrics.jobs_completed == 0
    assert metrics.jobs_failed == 1
    assert metrics.jobs_retried == 3

    await worker.stop()