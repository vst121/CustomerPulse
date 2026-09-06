from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.customers.customer_service import (
    CustomerAlreadyExistsError,
    CustomerService,
)
from app.domain.customers.entities import LifecycleStage
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.repositories.customer_repository import (
    PostgresCustomerRepository,
)
from app.schemas.customers import (
    CreateCustomerRequest,
    CustomerListResponse,
    CustomerResponse,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


def get_customer_service(
    session: AsyncSession = Depends(get_db_session),
) -> CustomerService:

    customer_repository = PostgresCustomerRepository(session)

    return CustomerService(
        customer_repository=customer_repository,
        session=session,
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