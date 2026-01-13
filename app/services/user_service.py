from sqlalchemy.orm import Session
from app.repositories.user_repository import user_repository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        return user_repository.create(db, user_in) # Add check for existing email/employee_id if needed, but DB constraint handles it

    def get_user(self, db: Session, user_id) -> User:
        return user_repository.get(db, user_id)

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return user_repository.get_multi(db, skip, limit)

    def update_user(self, db: Session, user: User, user_in: UserUpdate) -> User:
        return user_repository.update(db, user, user_in)
    
    def delete_user(self, db: Session, user_id) -> User:
        return user_repository.remove(db, user_id)

user_service = UserService()
