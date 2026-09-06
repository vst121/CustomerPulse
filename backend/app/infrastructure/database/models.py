from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint


class Base(DeclarativeBase):
    pass


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    lifecycle_stage: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ACQUISITION",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

class TransactionModel(Base):
    __tablename__ = "transactions"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "idempotency_key",
            name="uq_transaction_customer_idempotency_key",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )    

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )    

class CustomerValueModel(Base):

    __tablename__ = "customer_values"

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
        primary_key=True,
    )

    total_spend: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    transaction_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    ) 

class CustomerScoreModel(Base):
    __tablename__ = "customer_scores"

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
        primary_key=True,
    )

    score: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )    