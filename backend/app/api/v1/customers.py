from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.customers.customer_service import CustomerService
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.repositories.customer_repository import (
    PostgresCustomerRepository,
)
from app.schemas.customers import (
    CreateCustomerRequest,
    CustomerResponse,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


def get_customer_service(
    session: AsyncSession = Depends(get_db_session),
) -> CustomerService:

    repository = PostgresCustomerRepository(session)

    return CustomerService(repository)

@router.post(
    "",
    response_model=CustomerResponse,
)
async def create_customer(
    request: CreateCustomerRequest,
    service: CustomerService = Depends(get_customer_service),
):

    customer = await service.create_customer(
        first_name=request.first_name,
        last_name=request.last_name,
        email=str(request.email),
    )

    return customer

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
            status_code=404,
            detail="Customer not found",
        )

    return customer

@router.get(
    "",
    response_model=list[CustomerResponse],
)
async def get_customers(
    service: CustomerService = Depends(get_customer_service),
):

    return await service.get_customers()

