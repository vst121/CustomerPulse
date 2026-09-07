from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    background_max_queue_size: int = 1000
    background_max_retries: int = 3
    background_retry_delay: float = 0.1
    background_shutdown_timeout: float = 30.0

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            background_max_queue_size=int(
                os.getenv("BACKGROUND_MAX_QUEUE_SIZE", "1000")
            ),
            background_max_retries=int(
                os.getenv("BACKGROUND_MAX_RETRIES", "3")
            ),
            background_retry_delay=float(
                os.getenv("BACKGROUND_RETRY_DELAY", "0.1")
            ),
            background_shutdown_timeout=float(
                os.getenv("BACKGROUND_SHUTDOWN_TIMEOUT", "30.0")
            ),
        )