from sqlalchemy.orm import Session
from app.repositories.book_repository import book_repository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

class BookService:
    def create_book(self, db: Session, book_in: BookCreate) -> Book:
        # Before creating, if available_quantity is not set (it's not in Create schema usually),
        # set it equal to quantity.
        obj_data = book_in.model_dump()
        if "available_quantity" not in obj_data:
            obj_data["available_quantity"] = obj_data["quantity"]
        
        db_obj = Book(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_book(self, db: Session, book_id) -> Book:
        return book_repository.get(db, book_id)

    def get_books(self, db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
        return book_repository.get_multi(db, skip, limit)

    def get_books_by_section(self, db: Session, section_id: int, skip: int, limit: int) -> list[Book]:
        return book_repository.get_by_section(db, section_id, skip, limit)

    def get_available_books(self, db: Session, skip: int, limit: int) -> list[Book]:
        return book_repository.get_available(db, skip, limit)

    def update_book(self, db: Session, book: Book, book_in: BookUpdate) -> Book:
        return book_repository.update(db, book, book_in)

    def delete_book(self, db: Session, book_id) -> Book:
        return book_repository.remove(db, book_id)

book_service = BookService()
