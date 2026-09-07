from typing import Any

from app.application.common.background_job import BackgroundJob
from app.application.common.background_job_dispatcher import (
    BackgroundJobDispatcher,
)
from app.application.common.background_worker import BackgroundWorker


class BackgroundWorkerDispatcher(BackgroundJobDispatcher):
    def __init__(self, worker: BackgroundWorker):
        self._worker = worker

    async def dispatch(
        self,
        job: BackgroundJob,
        payload: dict[str, Any],
    ) -> None:
        await self._worker.enqueue(
            job,
            payload,
        )