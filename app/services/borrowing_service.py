from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.repositories.borrowing_repository import borrowing_repository
from app.repositories.book_repository import book_repository
from app.models.borrowing import BorrowingRecord, BorrowingStatus
from app.schemas.borrowing import BorrowingCreate, BorrowingReturn
from app.services.fine_service import fine_service
from app.schemas.fine import FineCreate
from app.core.config import settings

class BorrowingService:
    def borrow_book(self, db: Session, borrowing_in: BorrowingCreate) -> BorrowingRecord:
        # Check book availability
        book = book_repository.get(db, borrowing_in.book_id)
        if not book or book.available_quantity < 1:
            raise ValueError("Book not available")
        
        # Decrement quantity
        book.available_quantity -= 1
        db.add(book)
        db.commit() # Should be transactional ideally
        
        # Calculate due date based on period
        # Simple due date calculation could go here if not in model default or passed in
        # Expecting borrowing_in to have logic or defaults, for now let's assume due_date logic needs to serve
        # For simplicity, if due_date is not in schema (it isn't), calculate it.
        # But wait, schema BorrowingCreate doesn't have due_date, it has borrowing_period_days.
        # So we need to calculate due_date.

        # Create record
        # Note: Repository create expects schema, but schema doesn't match model 1:1 if we need to calc fields.
        # We might need to manually create the model or adjust schema/repo.
        # Let's adjust input to Repo or do it manually here.
        
        from datetime import timedelta
        due_date = datetime.now(timezone.utc) + timedelta(days=borrowing_in.borrowing_period_days)
        
        # We need to construct the model data manually since Repo Generic create might be too simple if schema mismatch
        # Or we add due_date to the params passed to repo if repo handles kwargs or if we map it.
        # Standard Generic Repo uses `obj_in.model_dump()`.
        # So we should probably update the valid dict or create model directly.
        
        db_obj = BorrowingRecord(
            book_id=borrowing_in.book_id,
            user_id=borrowing_in.user_id,
            due_date=due_date,
            status=BorrowingStatus.ACTIVE
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def return_book(self, db: Session, borrowing_id) -> BorrowingRecord:
        borrowing = borrowing_repository.get(db, borrowing_id)
        if not borrowing or borrowing.status != BorrowingStatus.ACTIVE:
            raise ValueError("Invalid borrowing record")

        # Update book availability
        book = book_repository.get(db, borrowing.book_id)
        if book:
            book.available_quantity += 1
            db.add(book)

        # Update borrowing status
        borrowing.returned_at = datetime.now(timezone.utc)
        borrowing.status = BorrowingStatus.RETURNED

        # Check for Overdue
        # Ensure datetimes are offset-aware or comparable
        # If due_date is naive (from DB), make it aware if needed, but usually SQLA handles it if configured.
        # Let's assume UTC.
        
        if borrowing.returned_at > borrowing.due_date:
            borrowing.status = BorrowingStatus.OVERDUE
            # Calculate Fine
            overdue_duration = borrowing.returned_at - borrowing.due_date
            days_overdue = overdue_duration.days
            if days_overdue > 0:
                amount = days_overdue * settings.FINE_RATE_PER_DAY
                fine_in = FineCreate(
                    borrowing_id=borrowing.id,
                    user_id=borrowing.user_id,
                    amount=amount
                )
                fine_service.create_fine(db, fine_in)

        db.add(borrowing)
        db.commit()
        db.refresh(borrowing)
        return borrowing

    def get_borrowing_history(self, db: Session, user_id) -> list[BorrowingRecord]:
        # Implement filtering logic in repo
        return borrowing_repository.get_active_by_user(db, user_id) # This is strictly active, need generic filter

borrowing_service = BorrowingService()
