from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from app.application.recommendations.recommendation_service import (
    RecommendationService,
)
from app.domain.customers.entities import Customer, LifecycleStage
from app.domain.scoring.entities import CustomerScore
from backend.tests.unit.application.test_customer_service import (
    FakeCustomerRepository,
)
from backend.tests.unit.application.test_unit_of_work import (
    FakeUnitOfWork,
)


class FakeCustomerScoreRepository:

    def __init__(self):
        self.items = {}

    async def get_by_customer_id(self, customer_id):
        return self.items.get(customer_id)

    async def add(self, customer_score):
        self.items[customer_score.customer_id] = customer_score
        return customer_score

    async def update(self, customer_score):
        self.items[customer_score.customer_id] = customer_score
        return customer_score


class FakeRecommendationRepository:

    def __init__(self):
        self.items = {}

    async def get_by_customer_id(self, customer_id):
        return [
            recommendation
            for recommendation in self.items.values()
            if recommendation.customer_id == customer_id
        ]

    async def add(self, recommendation):
        self.items[recommendation.id] = recommendation
        return recommendation


def create_test_customer(
    lifecycle_stage=LifecycleStage.ACQUISITION,
) -> Customer:

    return Customer(
        id=uuid4(),
        first_name="Anna",
        last_name="Müller",
        email=f"{uuid4()}@example.com",
        lifecycle_stage=lifecycle_stage,
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.anyio
async def test_high_score_generates_loyalty_reward():

    customer = create_test_customer()

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    score_repository = FakeCustomerScoreRepository()
    score_repository.items[customer.id] = CustomerScore(
        customer_id=customer.id,
        score=Decimal("85.00"),
    )

    recommendation_repository = FakeRecommendationRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=None,
        customer_score_repository=score_repository,
        recommendation_repository=recommendation_repository,
    )

    service = RecommendationService(uow=uow)

    recommendation = await service.generate_recommendation(
        customer.id
    )

    assert recommendation.type.value == "LOYALTY_REWARD"
    assert recommendation.customer_id == customer.id
    assert "high value score" in recommendation.reason
    assert uow.commit_count == 1

@pytest.mark.anyio
async def test_win_back_customer_generates_reactivation():

    customer = create_test_customer(
        lifecycle_stage=LifecycleStage.WIN_BACK,
    )

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    score_repository = FakeCustomerScoreRepository()

    recommendation_repository = FakeRecommendationRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=None,
        customer_score_repository=score_repository,
        recommendation_repository=recommendation_repository,
    )

    service = RecommendationService(uow=uow)

    recommendation = await service.generate_recommendation(
        customer.id
    )

    assert recommendation.type.value == "REACTIVATION"
    assert "WIN_BACK" in recommendation.reason


@pytest.mark.anyio
async def test_retention_customer_generates_retention_offer():

    customer = create_test_customer(
        lifecycle_stage=LifecycleStage.RETENTION,
    )

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    score_repository = FakeCustomerScoreRepository()
    score_repository.items[customer.id] = CustomerScore(
        customer_id=customer.id,
        score=Decimal("50.00"),
    )

    recommendation_repository = FakeRecommendationRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=None,
        customer_score_repository=score_repository,
        recommendation_repository=recommendation_repository,
    )

    service = RecommendationService(uow=uow)

    recommendation = await service.generate_recommendation(
        customer.id
    )

    assert recommendation.type.value == "RETENTION_OFFER"


@pytest.mark.anyio
async def test_medium_high_score_generates_upsell():

    customer = create_test_customer()

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    score_repository = FakeCustomerScoreRepository()
    score_repository.items[customer.id] = CustomerScore(
        customer_id=customer.id,
        score=Decimal("65.00"),
    )

    recommendation_repository = FakeRecommendationRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=None,
        customer_score_repository=score_repository,
        recommendation_repository=recommendation_repository,
    )

    service = RecommendationService(uow=uow)

    recommendation = await service.generate_recommendation(
        customer.id
    )

    assert recommendation.type.value == "UPSELL"


@pytest.mark.anyio
async def test_medium_score_generates_cross_sell():

    customer = create_test_customer()

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    score_repository = FakeCustomerScoreRepository()
    score_repository.items[customer.id] = CustomerScore(
        customer_id=customer.id,
        score=Decimal("45.00"),
    )

    recommendation_repository = FakeRecommendationRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=None,
        customer_score_repository=score_repository,
        recommendation_repository=recommendation_repository,
    )

    service = RecommendationService(uow=uow)

    recommendation = await service.generate_recommendation(
        customer.id
    )

    assert recommendation.type.value == "CROSS_SELL"


@pytest.mark.anyio
async def test_low_score_generates_no_action():

    customer = create_test_customer()

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    score_repository = FakeCustomerScoreRepository()
    score_repository.items[customer.id] = CustomerScore(
        customer_id=customer.id,
        score=Decimal("20.00"),
    )

    recommendation_repository = FakeRecommendationRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=None,
        customer_value_repository=None,
        customer_score_repository=score_repository,
        recommendation_repository=recommendation_repository,
    )

    service = RecommendationService(uow=uow)

    recommendation = await service.generate_recommendation(
        customer.id
    )

    assert recommendation.type.value == "NO_ACTION"    