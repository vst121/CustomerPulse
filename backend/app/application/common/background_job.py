from abc import ABC, abstractmethod
from typing import Any


class BackgroundJob(ABC):

    @abstractmethod
    async def execute(self, payload: dict[str, Any]) -> None:
        ...