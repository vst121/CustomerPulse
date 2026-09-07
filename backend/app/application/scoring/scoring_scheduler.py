from uuid import UUID

from app.application.common.background_job_dispatcher import (
    BackgroundJobDispatcher,
)
from app.application.scoring.customer_scoring_job import (
    CustomerScoringJob,
)


class CustomerScoringScheduler:
    def __init__(
        self,
        dispatcher: BackgroundJobDispatcher,
    ):
        self.dispatcher = dispatcher

    async def schedule(
        self,
        customer_id: UUID,
    ) -> None:
        job = CustomerScoringJob()

        await self.dispatcher.dispatch(
            job,
            {"customer_id": str(customer_id)},
        )