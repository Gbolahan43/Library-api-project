from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class SectionCreate(SectionBase):
    pass

class SectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Section(SectionBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
