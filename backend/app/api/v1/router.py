from fastapi import APIRouter

from app.api.v1.customers import router as customers_router
from app.api.v1.health import router as health_router


router = APIRouter()

router.include_router(health_router)
router.include_router(customers_router)