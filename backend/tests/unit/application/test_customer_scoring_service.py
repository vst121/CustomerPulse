from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from app.application.scoring.customer_scoring_service import (
    CustomerScoringService,
)
from app.domain.customers.entities import Customer, LifecycleStage
from app.domain.value.entities import CustomerValue
from backend.tests.unit.application.test_customer_service import (
    FakeCustomerRepository,
)
from backend.tests.unit.application.test_unit_of_work import FakeUnitOfWork


class FakeCustomerValueRepository:
    def __init__(self):
        self.items = {}

    async def get_by_customer_id(
        self,
        customer_id,
    ):
        return self.items.get(customer_id)

    async def add(
        self,
        customer_value,
    ):
        self.items[customer_value.customer_id] = customer_value
        return customer_value

    async def update(
        self,
        customer_value,
    ):
        self.items[customer_value.customer_id] = customer_value
        return customer_value


class FakeCustomerScoreRepository:
    def __init__(self):
        self.items = {}

    async def get_by_customer_id(
        self,
        customer_id,
    ):
        return self.items.get(customer_id)

    async def add(
        self,
        customer_score,
    ):
        self.items[customer_score.customer_id] = customer_score
        return customer_score

    async def update(
        self,
        customer_score,
    ):
        self.items[customer_score.customer_id] = customer_score
        return customer_score


def create_test_customer() -> Customer:
    return Customer(
        id=uuid4(),
        first_name="Anna",
        last_name="Müller",
        email=f"{uuid4()}@example.com",
        lifecycle_stage=LifecycleStage.ACQUISITION,
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.anyio
async def test_calculate_customer_score():
    customer = create_test_customer()

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    customer_value_repository = FakeCustomerValueRepository()
    customer_value_repository.items[customer.id] = CustomerValue(
        customer_id=customer.id,
        total_spend=Decimal("100.00"),
        transaction_count=1,
    )

    customer_score_repository = FakeCustomerScoreRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=customer_value_repository,
        customer_score_repository=customer_score_repository,
    )

    service = CustomerScoringService(uow=uow)

    customer_score = await service.calculate_score(customer.id)

    assert customer_score.customer_id == customer.id
    assert customer_score.score == Decimal("55.00")
    assert uow.commit_count == 1