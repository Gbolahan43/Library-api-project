from sqlalchemy.orm import Session
from app.repositories.book_repository import book_repository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

class BookService:
    def create_book(self, db: Session, book_in: BookCreate) -> Book:
        return book_repository.create(db, book_in)

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
