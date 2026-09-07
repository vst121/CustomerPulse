import asyncio
import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from app.application.common.background_job import BackgroundJob
from app.application.common.background_worker_options import (
    BackgroundWorkerOptions,
)

logger = logging.getLogger(__name__)


class BackgroundWorkerState(StrEnum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"


@dataclass
class BackgroundJobRequest:
    job: BackgroundJob
    payload: dict[str, Any]

@dataclass(frozen=True)
class BackgroundWorkerMetrics:
    jobs_started: int
    jobs_completed: int
    jobs_failed: int
    jobs_retried: int

class BackgroundWorker:
    def __init__(
        self,
        options: BackgroundWorkerOptions | None = None,
    ):        
        self._options = options or BackgroundWorkerOptions()
        self._queue: asyncio.Queue[BackgroundJobRequest] | None = None
        self._task: asyncio.Task[None] | None = None
        self._state = BackgroundWorkerState.STOPPED
        self._jobs_started = 0
        self._jobs_completed = 0
        self._jobs_failed = 0
        self._jobs_retried = 0        

    async def start(self) -> None:
        if self._state == BackgroundWorkerState.RUNNING:
            return

        if self._state == BackgroundWorkerState.STOPPING:
            raise RuntimeError(
                "BackgroundWorker is currently stopping."
            )

        self._queue = asyncio.Queue(
            maxsize=self._options.max_queue_size
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
            try:
                await asyncio.wait_for(
                    self._queue.join(),
                    timeout=self._options.shutdown_timeout,
                )
            except asyncio.TimeoutError:
                logger.warning(
                    "BackgroundWorker shutdown timed out after %.2f seconds.",
                    self._options.shutdown_timeout,
                )

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
                self._jobs_started += 1

                attempt = 0

                while True:
                    try:
                        await request.job.execute(request.payload)

                        self._jobs_completed += 1

                        break

                    except asyncio.CancelledError:
                        raise

                    except Exception:
                        attempt += 1

                        if attempt > self._options.max_retries:
                            self._jobs_failed += 1

                            logger.exception(
                                "Background job failed after %s retries.",
                                self._options.max_retries,
                            )

                            break

                        self._jobs_retried += 1

                        delay = self._options.retry_delay * (
                            2 ** (attempt - 1)
                        )

                        logger.exception(
                            "Background job failed. Retrying "
                            "(attempt %s/%s) in %.2f seconds.",
                            attempt,
                            self._options.max_retries,
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

    @property
    def metrics(self) -> BackgroundWorkerMetrics:
        return BackgroundWorkerMetrics(
            jobs_started=self._jobs_started,
            jobs_completed=self._jobs_completed,
            jobs_failed=self._jobs_failed,
            jobs_retried=self._jobs_retried,
        )

    @property
    def queue_size(self) -> int:
        if self._queue is None:
            return 0

        return self._queue.qsize()    

    @property
    def state(self) -> BackgroundWorkerState:
        return self._state    