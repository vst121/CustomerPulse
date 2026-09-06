from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Header,
    status,
)
from app.application.transactions.transaction_service import (
    TransactionService,
)
from app.infrastructure.database.database import get_db_session
from app.schemas.transactions import (
    CreateTransactionRequest,
    TransactionListResponse,
    TransactionResponse,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.unit_of_work import (
    PostgresUnitOfWork,
)
from app.application.scoring.customer_scoring_scheduler import (
    CustomerScoringScheduler,
)
from app.application.common.application_runtime import background_worker

def get_transaction_service(
    session: AsyncSession = Depends(get_db_session),
) -> TransactionService:

    uow = PostgresUnitOfWork(session)

    scoring_scheduler = CustomerScoringScheduler(
        worker=background_worker,
    )

    return TransactionService(
        uow=uow,
        scoring_scheduler=scoring_scheduler,
    )

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

@router.post(
    "/customers/{customer_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    customer_id: UUID,
    request: CreateTransactionRequest,
    idempotency_key: str = Header(
        ...,
        min_length=1,
        max_length=100,
    ),
        service: TransactionService = Depends(
        get_transaction_service
    ),
):

    return await service.create_transaction(
        customer_id=customer_id,
        idempotency_key=idempotency_key,
        amount=request.amount,
        currency=request.currency,
        category=request.category,
        status=request.status,
        timestamp=request.timestamp,
    )


@router.get(
    "/customers/{customer_id}",
    response_model=TransactionListResponse,
)
async def get_customer_transactions(
    customer_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    service: TransactionService = Depends(
        get_transaction_service
    ),
):

    transactions, total = (
        await service.get_customer_transactions(
            customer_id=customer_id,
            page=page,
            page_size=page_size,
        )
    )

    return TransactionListResponse(
        items=transactions,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
async def get_transaction(
    transaction_id: UUID,
    service: TransactionService = Depends(
        get_transaction_service
    ),
):

    transaction = await service.get_transaction(
        transaction_id
    )

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found.",
        )

    return transaction