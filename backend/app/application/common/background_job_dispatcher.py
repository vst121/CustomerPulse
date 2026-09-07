from abc import ABC, abstractmethod
from typing import Any

from app.application.common.background_job import BackgroundJob


class BackgroundJobDispatcher(ABC):
    @abstractmethod
    async def dispatch(
        self,
        job: BackgroundJob,
        payload: dict[str, Any],
    ) -> None:
        ...