from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.borrowing import BorrowingStatus
from app.schemas.fine import Fine

class BorrowingBase(BaseModel):
    book_id: UUID
    user_id: UUID

class BorrowingCreate(BorrowingBase):
    borrowing_period_days: Optional[int] = 14

class BorrowingReturn(BaseModel):
    borrowing_id: UUID

class Borrowing(BorrowingBase):
    id: UUID
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None
    status: BorrowingStatus
    created_at: datetime
    
    # Optional nested fine if we want to show it in response immediately
    # fine_generated: Optional[Fine] = None 

    model_config = ConfigDict(from_attributes=True)
