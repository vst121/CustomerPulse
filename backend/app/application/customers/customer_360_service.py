from uuid import UUID

from app.application.common.unit_of_work import UnitOfWork
from app.domain.value.entities import CustomerValue
from app.domain.scoring.entities import CustomerScore


class Customer360Service:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_customer_360(
        self,
        customer_id: UUID,
    ):
        async with self.uow:

            customer = await self.uow.customers.get_by_id(
                customer_id
            )

            if customer is None:
                raise ValueError(
                    f"Customer '{customer_id}' was not found."
                )

            customer_value = (
                await self.uow.customer_values.get_by_customer_id(
                    customer_id
                )
            )

            customer_score = (
                await self.uow.customer_scores.get_by_customer_id(
                    customer_id
                )
            )

            transactions, _ = (
                await self.uow.transactions.get_by_customer_id(
                    customer_id=customer_id,
                    page=1,
                    page_size=20,
                )
            )

            recommendations = (
                await self.uow.recommendations.get_by_customer_id(
                    customer_id
                )
            )

            return {
                "customer": customer,
                "value": customer_value
                or CustomerValue(
                    customer_id=customer_id,
                    total_spend=0,
                    transaction_count=0,
                ),
                "score": customer_score
                or CustomerScore(
                    customer_id=customer_id,
                    score=0,
                ),
                "transactions": transactions,
                "recommendations": recommendations,
            }