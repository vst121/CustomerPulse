from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.customers.customer_360_service import (
    Customer360Service,
)
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.unit_of_work import PostgresUnitOfWork

from app.api.v1.schemas.customer_360 import (
    Customer360Response,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customer 360"],
)


@router.get(
    "/{customer_id}/360",
    response_model=Customer360Response,
)
async def get_customer_360(
    customer_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    uow = PostgresUnitOfWork(session)

    service = Customer360Service(
        uow=uow
    )

    try:
        result = await service.get_customer_360(
            customer_id
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Customer '{customer_id}' was not found.",
        )

    customer = result["customer"]
    value = result["value"]
    score = result["score"]

    return Customer360Response(
        id=customer.id,
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
        lifecycle_stage=customer.lifecycle_stage.value,
        created_at=customer.created_at,
        value={
            "total_spend": value.total_spend,
            "transaction_count": value.transaction_count,
        },
        score={
            "score": score.score,
        },
        transactions=[
            {
                "id": transaction.id,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "category": transaction.category.value,
                "status": transaction.status.value,
                "timestamp": transaction.timestamp,
            }
            for transaction in result["transactions"]
        ],
        recommendations=[
            {
                "id": recommendation.id,
                "type": recommendation.type.value,
                "reason": recommendation.reason,
            }
            for recommendation in result["recommendations"]
        ],
    )