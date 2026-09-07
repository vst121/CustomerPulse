import asyncio

import pytest

from app.application.common.background_job import BackgroundJob
from app.application.common.background_worker import (
    BackgroundWorker,
    BackgroundWorkerState,
)


class TestJob(BackgroundJob):
    def __init__(
        self,
        completed: list[str],
        name: str,
    ):
        self.completed = completed
        self.name = name

    async def execute(self, payload: dict[str, object]) -> None:
        await asyncio.sleep(0.01)
        self.completed.append(self.name)

@pytest.mark.asyncio
async def test_start_is_idempotent() -> None:
    worker = BackgroundWorker()

    await worker.start()

    first_task = worker._task
    first_queue = worker._queue

    await worker.start()

    assert worker._state == BackgroundWorkerState.RUNNING
    assert worker._task is first_task
    assert worker._queue is first_queue

    await worker.stop()


@pytest.mark.asyncio
async def test_stop_is_idempotent() -> None:
    worker = BackgroundWorker()

    await worker.start()

    await worker.stop()
    await worker.stop()

    assert worker._state == BackgroundWorkerState.STOPPED
    assert worker._task is None
    assert worker._queue is None
    
@pytest.mark.asyncio
async def test_stop_drains_queued_jobs() -> None:
    worker = BackgroundWorker()

    completed: list[str] = []

    await worker.start()

    await worker.enqueue(
        TestJob(completed, "job-1"),
        {},
    )

    await worker.enqueue(
        TestJob(completed, "job-2"),
        {},
    )

    await worker.enqueue(
        TestJob(completed, "job-3"),
        {},
    )

    await worker.stop()

    assert completed == [
        "job-1",
        "job-2",
        "job-3",
    ]

    assert worker._state == BackgroundWorkerState.STOPPED


@pytest.mark.asyncio
async def test_enqueue_is_rejected_during_shutdown() -> None:
    worker = BackgroundWorker()

    completed: list[str] = []

    await worker.start()

    await worker.enqueue(
        TestJob(completed, "job-1"),
        {},
    )

    stop_task = asyncio.create_task(worker.stop())

    while worker._state != BackgroundWorkerState.STOPPING:
        await asyncio.sleep(0)

    with pytest.raises(RuntimeError, match="not running"):
        await worker.enqueue(
            TestJob(completed, "job-2"),
            {},
        )

    await stop_task

    assert completed == ["job-1"]
    assert worker._state == BackgroundWorkerState.STOPPED

