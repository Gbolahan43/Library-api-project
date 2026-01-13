from sqlalchemy.orm import Session
from app.repositories.section_repository import section_repository
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate

class SectionService:
    def create_section(self, db: Session, section_in: SectionCreate) -> Section:
        return section_repository.create(db, section_in)

    def get_section(self, db: Session, section_id) -> Section:
        return section_repository.get(db, section_id)
    
    def get_sections(self, db: Session, skip: int = 0, limit: int = 100) -> list[Section]:
        return section_repository.get_multi(db, skip, limit)

section_service = SectionService()
