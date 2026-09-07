import asyncio
import time
import pytest

from app.application.common.background_job import BackgroundJob
from app.application.common.background_worker import BackgroundWorker
from backend.app.application.common.background_worker_options import BackgroundWorkerOptions


class FailingJob(BackgroundJob):
    def __init__(self) -> None:
        self.attempts = 0

    async def execute(self, payload: dict[str, object]) -> None:
        self.attempts += 1
        raise RuntimeError("job failed")

class EventuallySuccessfulJob(BackgroundJob):
    def __init__(self, failures_before_success: int) -> None:
        self.attempts = 0
        self.failures_before_success = failures_before_success

    async def execute(self, payload: dict[str, object]) -> None:
        self.attempts += 1

        if self.attempts <= self.failures_before_success:
            raise RuntimeError("temporary failure")

class BlockingRetryJob(BackgroundJob):
    def __init__(self) -> None:
        self.attempts = 0

    async def execute(self, payload: dict[str, object]) -> None:
        self.attempts += 1
        raise RuntimeError("temporary failure")


@pytest.mark.asyncio
async def test_failed_job_is_retried_and_eventually_succeeds() -> None:
    worker = BackgroundWorker(
        options=BackgroundWorkerOptions(
            max_retries=3,
        ),
    )
    job = EventuallySuccessfulJob(failures_before_success=2)

    await worker.start()

    await worker.enqueue(job, {})

    await worker._queue.join()

    await worker.stop()

    assert job.attempts == 3


@pytest.mark.asyncio
async def test_failed_job_stops_after_max_retries() -> None:
    worker = BackgroundWorker(
        options=BackgroundWorkerOptions(
            max_retries=3,
        ),
    )
    job = FailingJob()

    await worker.start()

    await worker.enqueue(job, {})

    await worker._queue.join()

    await worker.stop()

    assert job.attempts == 4

@pytest.mark.asyncio
async def test_failed_job_uses_exponential_backoff() -> None:
    worker = BackgroundWorker(
        options=BackgroundWorkerOptions(
            max_retries=2,
            retry_delay=0.05,
        ),
    )

    job = FailingJob()

    await worker.start()

    started_at = time.monotonic()

    await worker.enqueue(job, {})

    await worker._queue.join()

    elapsed = time.monotonic() - started_at

    await worker.stop()

    assert job.attempts == 3

    # 0.05s + 0.10s = 0.15s minimum
    assert elapsed >= 0.15    

@pytest.mark.asyncio
async def test_shutdown_timeout_cancels_long_retry_backoff() -> None:
    worker = BackgroundWorker(
        options=BackgroundWorkerOptions(
            max_retries=10,
            retry_delay=10.0,
            shutdown_timeout=0.1,
        ),
    )

    job = BlockingRetryJob()

    await worker.start()
    await worker.enqueue(job, {})

    await asyncio.sleep(0.05)

    assert job.attempts == 1

    started_at = time.monotonic()

    await worker.stop()

    elapsed = time.monotonic() - started_at

    assert elapsed < 1.0
    assert job.attempts == 1