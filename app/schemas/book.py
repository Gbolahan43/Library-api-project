from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class BookBase(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    isbn: str
    publication_year: int
    publisher: Optional[str] = None
    section_id: int
    quantity: int = Field(gt=0)
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    section_id: Optional[int] = None
    quantity: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None

class BookUpdateQuantity(BaseModel):
    quantity: int = Field(gt=0)

class Book(BookBase):
    id: UUID
    available_quantity: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
