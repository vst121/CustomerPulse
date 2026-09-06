from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.customers import router as customers_router
from app.api.v1.transactions import (
    router as transactions_router,
)
from app.api.v1.scoring import router as scoring_router
from app.api.v1.recommendations import (
    router as recommendations_router,
)
from app.api.v1.customer_360 import router as customer_360_router

router = APIRouter()

router.include_router(health_router)
router.include_router(customers_router)
router.include_router(transactions_router)
router.include_router(scoring_router)
router.include_router(recommendations_router)
router.include_router(customer_360_router)
