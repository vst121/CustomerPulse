from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.scoring.customer_scoring_service import (
    CustomerScoringService,
)
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.unit_of_work import PostgresUnitOfWork


router = APIRouter(
    prefix="/customers",
    tags=["Scoring"],
)


@router.get("/{customer_id}/scores")
async def get_customer_score(
    customer_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    uow = PostgresUnitOfWork(session)
    service = CustomerScoringService(uow=uow)

    try:
        customer_score = await service.calculate_score(
            customer_id
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Customer '{customer_id}' was not found.",
        )

    return {
        "customer_id": customer_score.customer_id,
        "score": customer_score.score,
    }