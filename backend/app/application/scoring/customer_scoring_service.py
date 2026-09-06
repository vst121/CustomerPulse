from decimal import Decimal
from uuid import UUID

from app.application.common.unit_of_work import UnitOfWork
from app.domain.scoring.entities import CustomerScore


class CustomerScoringService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def calculate_score(
        self,
        customer_id: UUID,
    ) -> CustomerScore:
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

            if customer_value is None:
                score = Decimal("0")
            else:
                score = min(
                    Decimal("100"),
                    (
                        customer_value.total_spend * Decimal("0.5")
                        + customer_value.transaction_count * Decimal("5")
                    ),
                )

            customer_score = CustomerScore(
                customer_id=customer_id,
                score=score,
            )

            existing = (
                await self.uow.customer_scores.get_by_customer_id(
                    customer_id
                )
            )

            if existing is None:
                customer_score = (
                    await self.uow.customer_scores.add(
                        customer_score
                    )
                )
            else:
                customer_score = (
                    await self.uow.customer_scores.update(
                        customer_score
                    )
                )

            await self.uow.commit()

            return customer_score