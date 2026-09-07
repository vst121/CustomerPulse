import inspect

from app.application.common.background_job_dispatcher import (
    BackgroundJobDispatcher,
)


def test_background_job_dispatcher_is_abstract() -> None:
    assert inspect.isabstract(BackgroundJobDispatcher)