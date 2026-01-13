from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.fine import Fine, FinePayment
from app.services.fine_service import fine_service
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[Fine])
def read_fines(user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return fine_service.get_fines_by_user(db, user_id, skip=skip, limit=limit)

@router.put("/{fine_id}/pay", response_model=Fine)
def pay_fine(fine_id: UUID, payment: FinePayment, db: Session = Depends(get_db)):
    fine = fine_service.pay_fine(db, fine_id)
    if not fine:
         raise HTTPException(status_code=404, detail="Fine not found")
    return fine
