import asyncio

import pytest

from app.application.common.background_job import BackgroundJob
from app.application.common.background_worker import BackgroundWorker


class BlockingJob(BackgroundJob):
    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def execute(self, payload: dict) -> None:
        self.started.set()
        await self.release.wait()


class SuccessfulJob(BackgroundJob):
    def __init__(self) -> None:
        self.executed = asyncio.Event()

    async def execute(self, payload: dict) -> None:
        self.executed.set()


@pytest.mark.asyncio
async def test_enqueue_waits_when_queue_is_full() -> None:
    worker = BackgroundWorker(
        max_queue_size=1,
    )

    blocking_job = BlockingJob()

    await worker.start()

    await worker.enqueue(
        blocking_job,
        {},
    )

    await blocking_job.started.wait()

    second_job = SuccessfulJob()

    await worker.enqueue(
        second_job,
        {},
    )

    third_enqueue = asyncio.create_task(
        worker.enqueue(
            SuccessfulJob(),
            {},
        )
    )

    await asyncio.sleep(0)

    assert not third_enqueue.done()

    blocking_job.release.set()

    await asyncio.wait_for(
        third_enqueue,
        timeout=1.0,
    )

    await worker.stop()