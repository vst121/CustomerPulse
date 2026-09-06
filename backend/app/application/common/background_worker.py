import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from app.application.common.background_job import BackgroundJob

logger = logging.getLogger(__name__)


@dataclass
class BackgroundJobRequest:
    job: BackgroundJob
    payload: dict[str, Any]


class BackgroundWorker:
    def __init__(self, max_queue_size: int = 1000):
        self._max_queue_size = max_queue_size
        self._queue: asyncio.Queue[BackgroundJobRequest] | None = None
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self._task is not None:
            return

        # Create the queue inside the current event loop.
        self._queue = asyncio.Queue(
            maxsize=self._max_queue_size
        )

        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task is None:
            return

        self._task.cancel()

        try:
            await self._task
        except asyncio.CancelledError:
            pass

        self._task = None
        self._queue = None

    async def enqueue(
        self,
        job: BackgroundJob,
        payload: dict[str, Any],
    ) -> None:
        if self._queue is None:
            raise RuntimeError(
                "BackgroundWorker has not been started."
            )

        await self._queue.put(
            BackgroundJobRequest(
                job=job,
                payload=payload,
            )
        )

    async def _run(self) -> None:
        if self._queue is None:
            raise RuntimeError(
                "BackgroundWorker queue has not been initialized."
            )

        while True:
            request = await self._queue.get()

            try:
                await request.job.execute(request.payload)
            except Exception:
                logger.exception(
                    "Background job execution failed."
                )
            finally:
                self._queue.task_done()
