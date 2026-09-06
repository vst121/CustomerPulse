from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4
import pytest

from backend.app.domain.customers.entities import Customer, LifecycleStage
from backend.app.domain.transactions.entities import TransactionCategory, TransactionStatus
from backend.tests.unit.application.test_customer_service import FakeCustomerRepository
from backend.tests.unit.application.test_unit_of_work import FakeUnitOfWork
from app.application.transactions.transaction_service import TransactionService


class FakeTransactionRepository:
    def __init__(self):
        self.items = {}

    async def get_by_idempotency_key(
        self,
        customer_id,
        idempotency_key,
    ):
        for transaction in self.items.values():
            if (
                transaction.customer_id == customer_id
                and transaction.idempotency_key == idempotency_key
            ):
                return transaction

        return None

    async def add(self, transaction):
        self.items[transaction.id] = transaction
        return transaction

class FakeCustomerValueRepository:
    def __init__(self):
        self.items = {}

    async def get_by_customer_id(self, customer_id):
        return self.items.get(customer_id)

    async def add(self, customer_value):
        self.items[customer_value.customer_id] = customer_value
        return customer_value

    async def update(self, customer_value):
        self.items[customer_value.customer_id] = customer_value
        return customer_value

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
async def test_completed_transaction_updates_customer_value():
    customer = create_test_customer()

    customer_repository = FakeCustomerRepository()
    customer_repository.customers.append(customer)

    transaction_repository = FakeTransactionRepository()
    customer_value_repository = FakeCustomerValueRepository()

    uow = FakeUnitOfWork(
        customer_repository=customer_repository,
        transaction_repository=transaction_repository,
        customer_value_repository=customer_value_repository,
    )

    service = TransactionService(uow=uow)

    transaction = await service.create_transaction(
        customer_id=customer.id,
        amount=Decimal("100.00"),
        currency="EUR",
        category=TransactionCategory.GROCERIES,
        status=TransactionStatus.COMPLETED,
        timestamp=datetime.now(timezone.utc),
        idempotency_key="test-value-001",
    )

    customer_value = (
        await customer_value_repository.get_by_customer_id(
            customer.id
        )
    )

    assert customer_value is not None
    assert customer_value.total_spend == Decimal("100.00")
    assert customer_value.transaction_count == 1
    assert transaction.customer_id == customer.id
    assert uow.commit_count == 1