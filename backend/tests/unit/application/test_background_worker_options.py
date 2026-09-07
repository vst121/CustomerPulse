import pytest

from app.application.common.background_worker_options import (
    BackgroundWorkerOptions,
)


def test_default_options_are_valid() -> None:
    options = BackgroundWorkerOptions()

    assert options.max_queue_size == 1000
    assert options.max_retries == 3
    assert options.retry_delay == 0.1
    assert options.shutdown_timeout == 30.0


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_queue_size": 0},
        {"max_queue_size": -1},
        {"max_retries": -1},
        {"retry_delay": -1},
        {"shutdown_timeout": -1},
    ],
)
def test_invalid_options_are_rejected(
    kwargs: dict,
) -> None:
    with pytest.raises(ValueError):
        BackgroundWorkerOptions(**kwargs)

def test_options_are_immutable() -> None:
    options = BackgroundWorkerOptions()

    with pytest.raises(AttributeError):
        options.max_retries = 10        