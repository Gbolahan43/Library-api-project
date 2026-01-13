from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from app.repositories.base import CRUDRepository
from app.models.borrowing import BorrowingRecord, BorrowingStatus
from app.schemas.borrowing import BorrowingCreate, BorrowingReturn

class BorrowingRepository(CRUDRepository[BorrowingRecord, BorrowingCreate, BorrowingReturn]):
    def get_active_by_user(self, db: Session, user_id: UUID) -> List[BorrowingRecord]:
        stmt = select(BorrowingRecord).where(
            BorrowingRecord.user_id == user_id, 
            BorrowingRecord.status == BorrowingStatus.ACTIVE
        )
        return db.execute(stmt).scalars().all()

    def get_overdue(self, db: Session, skip: int = 0, limit: int = 100) -> List[BorrowingRecord]:
        stmt = select(BorrowingRecord).where(
            BorrowingRecord.status == BorrowingStatus.OVERDUE
        ).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

borrowing_repository = BorrowingRepository(BorrowingRecord)
