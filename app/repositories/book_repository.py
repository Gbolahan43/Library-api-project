from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base import CRUDRepository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

class BookRepository(CRUDRepository[Book, BookCreate, BookUpdate]):
    def get_by_isbn(self, db: Session, isbn: str) -> Optional[Book]:
        stmt = select(Book).where(Book.isbn == isbn)
        return db.execute(stmt).scalars().first()

    def get_by_section(self, db: Session, section_id: int, skip: int = 0, limit: int = 100) -> List[Book]:
        stmt = select(Book).where(Book.section_id == section_id).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def get_available(self, db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
        stmt = select(Book).where(Book.available_quantity > 0).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

book_repository = BookRepository(Book)
