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
        self._queue: asyncio.Queue[BackgroundJobRequest] = asyncio.Queue(
            maxsize=max_queue_size
        )
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self._task is not None:
            return

        self._task = asyncio.create_task(
            self._run()
        )

    async def stop(self) -> None:
        if self._task is None:
            return

        self._task.cancel()

        try:
            await self._task
        except asyncio.CancelledError:
            pass

        self._task = None

    async def enqueue(
        self,
        job: BackgroundJob,
        payload: dict[str, Any],
    ) -> None:
        await self._queue.put(
            BackgroundJobRequest(
                job=job,
                payload=payload,
            )
        )

    async def _run(self) -> None:
        while True:
            request = await self._queue.get()

            try:
                await request.job.execute(
                    request.payload
                )
            except Exception:
                logger.exception(
                    "Background job execution failed."
                )
            finally:
                self._queue.task_done()