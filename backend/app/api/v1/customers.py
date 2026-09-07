from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.customers.customer_service import (
    CustomerAlreadyExistsError,
    CustomerService,
)
from app.domain.customers.entities import LifecycleStage
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.unit_of_work import PostgresUnitOfWork
from app.schemas.customers import (
    CreateCustomerRequest,
    CustomerListResponse,
    CustomerResponse,
)
from app.application.recommendations.customer_decision_engine import (
    CustomerDecisionEngine,
)
from app.application.recommendations.next_best_action_service import (
    NextBestActionService,
)
from app.application.scoring.customer_feature_extractor import (
    CustomerFeatureExtractor,
)
from app.application.scoring.customer_intelligence_service import (
    CustomerIntelligenceService,
)
from app.application.scoring.deterministic_customer_predictor import (
    DeterministicCustomerPredictor,
)
from app.schemas.customer_intelligence import (
    CustomerIntelligenceResponse,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


def get_customer_service(
    session: AsyncSession = Depends(get_db_session),
) -> CustomerService:

    uow = PostgresUnitOfWork(session)

    return CustomerService(
        uow=uow,
    )

def get_customer_intelligence_service(
    session: AsyncSession = Depends(get_db_session),
) -> CustomerIntelligenceService:

    uow = PostgresUnitOfWork(session)

    return CustomerIntelligenceService(
        uow=uow,
        feature_extractor=CustomerFeatureExtractor(),
        predictor=DeterministicCustomerPredictor(),
        decision_engine=CustomerDecisionEngine(),
        action_service=NextBestActionService(),
    )

@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    request: CreateCustomerRequest,
    service: CustomerService = Depends(get_customer_service),
):

    try:
        return await service.create_customer(
            first_name=request.first_name,
            last_name=request.last_name,
            email=str(request.email),
        )

    except CustomerAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def get_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
):

    customer = await service.get_customer(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    return customer


@router.get(
    "",
    response_model=CustomerListResponse,
)
async def get_customers(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
    ),
    lifecycle_stage: LifecycleStage | None = None,
    service: CustomerService = Depends(get_customer_service),
):

    customers, total = await service.get_customers(
        page=page,
        page_size=page_size,
        search=search,
        lifecycle_stage=lifecycle_stage,
    )

    return CustomerListResponse(
        items=customers,
        page=page,
        page_size=page_size,
        total=total,
    )

@router.get(
    "/{customer_id}/intelligence",
    response_model=CustomerIntelligenceResponse,
)
async def get_customer_intelligence(
    customer_id: UUID,
    service: CustomerIntelligenceService = Depends(
        get_customer_intelligence_service
    ),
):
    result = await service.analyze(customer_id)

    return CustomerIntelligenceResponse(
        features={
            "transaction_count": result.features.transaction_count,
            "total_transaction_value": result.features.total_transaction_value,
            "average_transaction_value": result.features.average_transaction_value,
            "days_since_last_transaction": (
                result.features.days_since_last_transaction
            ),
        },
        prediction={
            "churn_probability": result.prediction.churn_probability,
        },
        action={
            "action_type": result.action.action_type,
            "priority": result.action.priority,
            "reason": result.action.reason,
        },
    )