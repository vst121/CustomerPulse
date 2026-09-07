import asyncio
import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from app.application.common.background_job import BackgroundJob


logger = logging.getLogger(__name__)


class BackgroundWorkerState(StrEnum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"


@dataclass
class BackgroundJobRequest:
    job: BackgroundJob
    payload: dict[str, Any]


class BackgroundWorker:
    def __init__(
        self,
        max_queue_size: int = 1000,
        max_retries: int = 3,
        retry_delay: float = 0.1,
    ):        
        self._max_queue_size = max_queue_size
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._queue: asyncio.Queue[BackgroundJobRequest] | None = None
        self._task: asyncio.Task[None] | None = None
        self._state = BackgroundWorkerState.STOPPED

    async def start(self) -> None:
        if self._state == BackgroundWorkerState.RUNNING:
            return

        if self._state == BackgroundWorkerState.STOPPING:
            raise RuntimeError(
                "BackgroundWorker is currently stopping."
            )

        self._queue = asyncio.Queue(
            maxsize=self._max_queue_size
        )

        self._task = asyncio.create_task(self._run())
        self._state = BackgroundWorkerState.RUNNING

    async def stop(self) -> None:
        if self._state == BackgroundWorkerState.STOPPED:
            return

        if self._state == BackgroundWorkerState.STOPPING:
            return

        self._state = BackgroundWorkerState.STOPPING

        if self._queue is not None:
            await self._queue.join()

        if self._task is not None:
            self._task.cancel()

            try:
                await self._task
            except asyncio.CancelledError:
                pass

        self._task = None
        self._queue = None
        self._state = BackgroundWorkerState.STOPPED
                
    async def enqueue(
        self,
        job: BackgroundJob,
        payload: dict[str, Any],
    ) -> None:
        if self._state != BackgroundWorkerState.RUNNING:
            raise RuntimeError(
                "BackgroundWorker is not running."
            )

        if self._queue is None:
            raise RuntimeError(
                "BackgroundWorker queue has not been initialized."
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
                attempt = 0

                while True:
                    try:
                        await request.job.execute(request.payload)
                        break

                    except asyncio.CancelledError:
                        raise

                    except Exception:
                        attempt += 1

                        if attempt > self._max_retries:
                            logger.exception(
                                "Background job failed after %s retries.",
                                self._max_retries,
                            )
                            break

                        delay = self._retry_delay * (2 ** (attempt - 1))

                        logger.exception(
                            "Background job failed. Retrying "
                            "(attempt %s/%s) in %.2f seconds.",
                            attempt,
                            self._max_retries,
                            delay,
                        )

                        await asyncio.sleep(delay)

            finally:
                self._queue.task_done()

            if (
                self._state == BackgroundWorkerState.STOPPING
                and self._queue.empty()
            ):
                break