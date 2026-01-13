from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    employee_id: Optional[str] = None
    role: str = "Librarian"

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
