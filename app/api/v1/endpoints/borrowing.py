from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.borrowing import Borrowing, BorrowingCreate, BorrowingReturn
from app.services.borrowing_service import borrowing_service
from typing import List

router = APIRouter()

@router.post("/", response_model=Borrowing, status_code=status.HTTP_201_CREATED)
def borrow_book(borrowing_in: BorrowingCreate, db: Session = Depends(get_db)):
    try:
        return borrowing_service.borrow_book(db, borrowing_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{borrowing_id}/return", response_model=Borrowing)
def return_book(borrowing_id: str, db: Session = Depends(get_db)):
    try:
        return borrowing_service.return_book(db, borrowing_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=List[Borrowing])
def read_user_borrowing_history(user_id: str, db: Session = Depends(get_db)):
    return borrowing_service.get_borrowing_history(db, user_id)

# Optional: Get by ID
