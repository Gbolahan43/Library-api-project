from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.section import Section, SectionCreate, SectionUpdate
from app.services.section_service import section_service
from typing import List

router = APIRouter()

@router.post("/", response_model=Section, status_code=status.HTTP_201_CREATED)
def create_section(section_in: SectionCreate, db: Session = Depends(get_db)):
    try:
        return section_service.create_section(db, section_in)
    except Exception as e:
        # Check for integrity error (duplicate name)
        # SQLAlchemy wraps the underlying DB error
        if "UNIQUE constraint failed" in str(e) or "IntegrityError" in str(type(e).__name__):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Section with this name already exists."
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Section])
def read_sections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return section_service.get_sections(db, skip=skip, limit=limit)

@router.get("/{section_id}", response_model=Section)
def read_section(section_id: int, db: Session = Depends(get_db)):
    section = section_service.get_section(db, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.delete("/{section_id}", response_model=Section)
def delete_section(section_id: int, db: Session = Depends(get_db)):
    section = section_service.get_section(db, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section_service.delete_section(db, section_id)
