from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.fine import FineStatus

class FineBase(BaseModel):
    amount: float = Field(gt=0)
    due_date: Optional[datetime] = None
    status: FineStatus = FineStatus.PENDING
    notes: Optional[str] = None

class FineCreate(FineBase):
    borrowing_id: UUID
    user_id: UUID

class FineUpdate(BaseModel):
    status: Optional[FineStatus] = None
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None

class FinePayment(BaseModel):
    payment_method: str = "Cash" # Simple placeholder
    notes: Optional[str] = None

class Fine(FineBase):
    id: UUID
    borrowing_id: UUID
    user_id: UUID
    fine_date: datetime
    paid_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
