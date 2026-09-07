from dataclasses import dataclass


@dataclass(frozen=True)
class BackgroundWorkerOptions:
    max_queue_size: int = 1000
    max_retries: int = 3
    retry_delay: float = 0.1
    shutdown_timeout: float = 30.0