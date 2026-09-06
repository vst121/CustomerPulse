import asyncio
from typing import Any

import pytest

from app.application.common.background_job import BackgroundJob
from app.application.common.background_worker import BackgroundWorker


class RecordingJob(BackgroundJob):

    def __init__(self):
        self.payloads: list[dict[str, Any]] = []

    async def execute(
        self,
        payload: dict[str, Any],
    ) -> None:
        self.payloads.append(payload)


@pytest.mark.asyncio
async def test_worker_executes_enqueued_job() -> None:
    worker = BackgroundWorker()

    job = RecordingJob()

    await worker.start()

    await worker.enqueue(
        job,
        {"customer_id": "123"},
    )

    await asyncio.sleep(0)

    await worker.stop()

    assert job.payloads == [
        {"customer_id": "123"}
    ]


@pytest.mark.asyncio
async def test_worker_processes_multiple_jobs() -> None:
    worker = BackgroundWorker()

    job = RecordingJob()

    await worker.start()

    await worker.enqueue(
        job,
        {"customer_id": "123"},
    )

    await worker.enqueue(
        job,
        {"customer_id": "456"},
    )

    await worker.enqueue(
        job,
        {"customer_id": "789"},
    )

    await asyncio.sleep(0)

    await worker.stop()

    assert job.payloads == [
        {"customer_id": "123"},
        {"customer_id": "456"},
        {"customer_id": "789"},
    ]