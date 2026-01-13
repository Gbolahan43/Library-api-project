from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base import CRUDRepository
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate

class SectionRepository(CRUDRepository[Section, SectionCreate, SectionUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Section]:
        stmt = select(Section).where(Section.name == name)
        return db.execute(stmt).scalars().first()

section_repository = SectionRepository(Section)
