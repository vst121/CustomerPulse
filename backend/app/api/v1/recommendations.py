from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.recommendations.recommendation_service import (
    RecommendationService,
)
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.unit_of_work import PostgresUnitOfWork


router = APIRouter(
    prefix="/customers",
    tags=["Recommendations"],
)


@router.get("/{customer_id}/recommendations")
async def get_customer_recommendations(
    customer_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    uow = PostgresUnitOfWork(session)

    customer = await uow.customers.get_by_id(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer '{customer_id}' was not found.",
        )

    recommendations = (
        await uow.recommendations.get_by_customer_id(
            customer_id
        )
    )

    return [
        {
            "id": recommendation.id,
            "customer_id": recommendation.customer_id,
            "type": recommendation.type,
            "reason": recommendation.reason,
        }
        for recommendation in recommendations
    ]


@router.post("/{customer_id}/recommendations/generate")
async def generate_customer_recommendation(
    customer_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    uow = PostgresUnitOfWork(session)
    service = RecommendationService(uow=uow)

    try:
        recommendation = (
            await service.generate_recommendation(
                customer_id
            )
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Customer '{customer_id}' was not found.",
        )

    return {
        "id": recommendation.id,
        "customer_id": recommendation.customer_id,
        "type": recommendation.type,
        "reason": recommendation.reason,
    }