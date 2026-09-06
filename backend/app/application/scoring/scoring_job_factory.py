from uuid import UUID

from app.application.common.background_job import BackgroundJob
from app.application.scoring.customer_scoring_job import CustomerScoringJob
from app.application.scoring.customer_scoring_service import (
    CustomerScoringService,
)


def create_customer_scoring_job(
    customer_id: UUID,
    scoring_service: CustomerScoringService,
) -> tuple[BackgroundJob, dict[str, str]]:
    job = CustomerScoringJob(
        scoring_service=scoring_service,
    )

    payload = {
        "customer_id": str(customer_id),
    }

    return job, payload