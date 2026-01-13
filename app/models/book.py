import uuid
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    publication_year = Column(Integer)
    publisher = Column(String)
    # Using String for section in Book table to align with simple Enum usage or FK if linking strictly.
    # Spec says "Section - Enum". Let's stick to string for simplicity based on "Enum" description or link to Section table if we strictly follow "Book Sections Table".
    # Spec 3.2 says "Books <-> Sections: Many-to-One". So it should be a FK.
    section_id = Column(Integer, ForeignKey("sections.id")) 
    
    quantity = Column(Integer, default=1)
    available_quantity = Column(Integer, default=1)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    section = relationship("Section", backref="books")
