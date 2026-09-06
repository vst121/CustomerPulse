from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customers.entities import Customer, LifecycleStage
from app.domain.customers.repositories import CustomerRepository
from app.infrastructure.database.models import CustomerModel



class PostgresCustomerRepository(CustomerRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        result = await self._session.execute(
            select(CustomerModel).where(
                CustomerModel.id == customer_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def get_all(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        lifecycle_stage: LifecycleStage | None = None,
    ) -> tuple[list[Customer], int]:

        query = select(CustomerModel)

        if search:
            search_pattern = f"%{search}%"

            query = query.where(
                or_(
                    CustomerModel.first_name.ilike(search_pattern),
                    CustomerModel.last_name.ilike(search_pattern),
                    CustomerModel.email.ilike(search_pattern),
                )
            )

        if lifecycle_stage:
            query = query.where(
                CustomerModel.lifecycle_stage
                == lifecycle_stage.value
            )

        count_query = select(
            func.count()
        ).select_from(
            query.subquery()
        )

        count_result = await self._session.execute(count_query)

        total = count_result.scalar_one()

        offset = (page - 1) * page_size

        query = (
            query
            .order_by(CustomerModel.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        result = await self._session.execute(query)

        models = result.scalars().all()

        customers = [
            self._to_domain(model)
            for model in models
        ]

        return customers, total

    async def add(
        self,
        customer: Customer,
    ) -> Customer:

        model = CustomerModel(
            id=customer.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            lifecycle_stage=customer.lifecycle_stage.value,
            created_at=customer.created_at,
        )

        self._session.add(model)

        await self._session.flush()

        return self._to_domain(model)

    async def exists_by_email(
        self,
        email: str,
    ) -> bool:

        result = await self._session.execute(
            select(CustomerModel.id)
            .where(CustomerModel.email == email)
            .limit(1)
        )

        return result.scalar_one_or_none() is not None

    async def exists(self, customer_id: UUID) -> bool:
        statement = (
            select(CustomerModel.id)
            .where(CustomerModel.id == customer_id)
            .limit(1)
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none() is not None    

    @staticmethod
    def _to_domain(
        model: CustomerModel,
    ) -> Customer:

        return Customer(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            lifecycle_stage=LifecycleStage(
                model.lifecycle_stage
            ),
            created_at=model.created_at,
        )

