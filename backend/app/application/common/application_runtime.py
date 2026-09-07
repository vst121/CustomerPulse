from app.application.common.background_worker import BackgroundWorker
from app.application.common.background_worker_dispatcher import (
    BackgroundWorkerDispatcher,
)
from app.config.settings import Settings


settings = Settings.from_environment()

background_worker_options = (
    settings.create_background_worker_options()
)

background_worker = BackgroundWorker(
    options=background_worker_options,
)

background_job_dispatcher = BackgroundWorkerDispatcher(
    worker=background_worker,
)