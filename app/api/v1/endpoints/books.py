from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.book import Book, BookCreate, BookUpdate
from app.services.book_service import book_service
from typing import List

router = APIRouter()

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book_in)

@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return book_service.get_books(db, skip=skip, limit=limit)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: str, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: str, book_in: BookUpdate, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_service.update_book(db, book, book_in)

@router.delete("/{book_id}", response_model=Book)
def delete_book(book_id: str, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_service.delete_book(db, book_id)

@router.get("/available", response_model=List[Book])
def read_available_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return book_service.get_available_books(db, skip=skip, limit=limit)
