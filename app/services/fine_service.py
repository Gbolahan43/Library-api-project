from sqlalchemy.orm import Session
from app.repositories.fine_repository import fine_repository
from app.models.fine import Fine, FineStatus
from app.schemas.fine import FineCreate, FineUpdate

class FineService:
    def create_fine(self, db: Session, fine_in: FineCreate) -> Fine:
        return fine_repository.create(db, fine_in)

    def get_fine(self, db: Session, fine_id) -> Fine:
        return fine_repository.get(db, fine_id)

    def get_fines_by_user(self, db: Session, user_id, skip: int, limit: int) -> list[Fine]:
        return fine_repository.get_by_user(db, user_id, skip, limit)

    def pay_fine(self, db: Session, fine_id) -> Fine:
        fine = fine_repository.get(db, fine_id)
        if fine:
             # Logic to record payment date etc can be added here
             update_data = FineUpdate(status=FineStatus.PAID)
             return fine_repository.update(db, fine, update_data)
        return None

fine_service = FineService()
