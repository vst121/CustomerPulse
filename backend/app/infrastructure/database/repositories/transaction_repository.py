from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.transactions.entities import (
    Transaction,
    TransactionCategory,
    TransactionStatus,
)
from app.domain.transactions.repositories import (
    TransactionRepository,
)
from app.infrastructure.database.models import TransactionModel


class PostgresTransactionRepository(TransactionRepository):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def get_by_id(
        self,
        transaction_id: UUID,
    ) -> Transaction | None:

        result = await self._session.execute(
            select(TransactionModel).where(
                TransactionModel.id == transaction_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def get_by_customer_id(
        self,
        customer_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[Transaction], int]:

        base_query = select(TransactionModel).where(
            TransactionModel.customer_id == customer_id
        )

        count_query = select(
            func.count()
        ).select_from(
            base_query.subquery()
        )

        count_result = await self._session.execute(
            count_query
        )

        total = count_result.scalar_one()

        offset = (page - 1) * page_size

        query = (
            base_query
            .order_by(TransactionModel.timestamp.desc())
            .offset(offset)
            .limit(page_size)
        )

        result = await self._session.execute(query)

        models = result.scalars().all()

        return (
            [self._to_domain(model) for model in models],
            total,
        )

    async def add(
        self,
        transaction: Transaction,
    ) -> Transaction:

        model = TransactionModel(
            id=transaction.id,
            customer_id=transaction.customer_id,
            amount=transaction.amount,
            currency=transaction.currency,
            category=transaction.category.value,
            status=transaction.status.value,
            timestamp=transaction.timestamp,
            idempotency_key=transaction.idempotency_key,
        )

        self._session.add(model)

        try:
            await self._session.flush()

        except IntegrityError as exc:
            await self._session.rollback()

            constraint_name = (
                "uq_transaction_customer_idempotency_key"
                if "uq_transaction_customer_idempotency_key"
                in str(exc.orig)
                else None
            )

            if (
                constraint_name
                == "uq_transaction_customer_idempotency_key"
            ):
                return await self._handle_idempotency_conflict(
                    transaction
                )

            raise

        return self._to_domain(model)

    async def get_by_idempotency_key(
        self,
        customer_id: UUID,
        idempotency_key: str,
    ) -> Transaction | None:

        result = await self._session.execute(
            select(TransactionModel).where(
                TransactionModel.customer_id == customer_id,
                TransactionModel.idempotency_key == idempotency_key,
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def _handle_idempotency_conflict(
        self,
        transaction: Transaction,
    ) -> Transaction:

        existing = await self.get_by_idempotency_key(
            customer_id=transaction.customer_id,
            idempotency_key=transaction.idempotency_key,
        )

        if existing is None:
            raise RuntimeError(
                "Transaction idempotency conflict occurred, "
                "but the existing transaction could not be found."
            )

        return existing    

    @staticmethod
    def _to_domain(
        model: TransactionModel,
    ) -> Transaction:

        return Transaction(
            id=model.id,
            customer_id=model.customer_id,
            idempotency_key=model.idempotency_key,
            amount=model.amount,
            currency=model.currency,
            category=TransactionCategory(model.category),
            status=TransactionStatus(model.status),
            timestamp=model.timestamp,
        )

