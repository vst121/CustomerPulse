from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.unit_of_work import UnitOfWork
from app.infrastructure.database.repositories.customer_repository import (
    PostgresCustomerRepository,
)
from app.infrastructure.database.repositories.transaction_repository import (
    PostgresTransactionRepository,
)
from app.infrastructure.database.repositories.customer_value_repository import (
    PostgresCustomerValueRepository,
)
from app.infrastructure.database.repositories.customer_score_repository import (
    PostgresCustomerScoreRepository,
)

class PostgresUnitOfWork(UnitOfWork):

    def __init__(self, session: AsyncSession):
        self._session = session

        self.customers = PostgresCustomerRepository(session)
        self.transactions = PostgresTransactionRepository(session)
        self.customer_values = PostgresCustomerValueRepository(session)    
        self.customer_scores = PostgresCustomerScoreRepository(session)            

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()