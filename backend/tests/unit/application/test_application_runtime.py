from app.application.common.application_runtime import (
    background_worker,
)


def test_background_worker_uses_configured_options() -> None:
    assert background_worker._options.max_queue_size == 1000
    assert background_worker._options.max_retries == 3
    assert background_worker._options.retry_delay == 0.1
    assert background_worker._options.shutdown_timeout == 30.0