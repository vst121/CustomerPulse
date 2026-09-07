from dataclasses import dataclass


@dataclass(frozen=True)
class BackgroundWorkerOptions:
    max_queue_size: int = 1000
    max_retries: int = 3
    retry_delay: float = 0.1
    shutdown_timeout: float = 30.0

    def __post_init__(self) -> None:
        if self.max_queue_size <= 0:
            raise ValueError(
                "max_queue_size must be greater than zero."
            )

        if self.max_retries < 0:
            raise ValueError(
                "max_retries must be greater than or equal to zero."
            )

        if self.retry_delay < 0:
            raise ValueError(
                "retry_delay must be greater than or equal to zero."
            )

        if self.shutdown_timeout < 0:
            raise ValueError(
                "shutdown_timeout must be greater than or equal to zero."
            )