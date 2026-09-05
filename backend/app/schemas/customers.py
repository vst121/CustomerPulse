from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateCustomerRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class CustomerResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    lifecycle_stage: str
    created_at: datetime