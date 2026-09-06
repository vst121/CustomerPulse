from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.application.common.background_worker import BackgroundWorker


background_worker = BackgroundWorker()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await background_worker.start()

    yield

    await background_worker.stop()


app = FastAPI(
    title="CustomerPulse API",
    description="Customer Lifecycle & Value Management Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(
    api_v1_router,
    prefix="/api/v1",
)