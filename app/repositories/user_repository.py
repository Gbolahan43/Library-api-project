from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base import CRUDRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(CRUDRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalars().first()

    def get_by_employee_id(self, db: Session, employee_id: str) -> Optional[User]:
        stmt = select(User).where(User.employee_id == employee_id)
        return db.execute(stmt).scalars().first()

user_repository = UserRepository(User)
