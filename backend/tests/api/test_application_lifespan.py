from fastapi.testclient import TestClient

from app.main import app, background_worker


def test_application_starts_and_stops_background_worker() -> None:
    assert background_worker._task is None
    assert background_worker._queue is None

    with TestClient(app):
        assert background_worker._task is not None
        assert not background_worker._task.done()
        assert background_worker._queue is not None

    assert background_worker._task is None
    assert background_worker._queue is None
