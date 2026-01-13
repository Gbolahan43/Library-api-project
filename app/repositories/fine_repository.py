from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from app.repositories.base import CRUDRepository
from app.models.fine import Fine, FineStatus
from app.schemas.fine import FineCreate, FineUpdate

class FineRepository(CRUDRepository[Fine, FineCreate, FineUpdate]):
    def get_by_user(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Fine]:
        stmt = select(Fine).where(Fine.user_id == user_id).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def get_outstanding_by_user(self, db: Session, user_id: UUID) -> List[Fine]:
        stmt = select(Fine).where(
            Fine.user_id == user_id,
            Fine.status.in_([FineStatus.PENDING, FineStatus.OVERDUE])
        )
        return db.execute(stmt).scalars().all()

fine_repository = FineRepository(Fine)
