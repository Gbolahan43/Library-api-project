import uuid
import enum
from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class BorrowingStatus(str, enum.Enum):
    ACTIVE = "Active"
    RETURNED = "Returned"
    OVERDUE = "Overdue"

class BorrowingRecord(Base):
    __tablename__ = "borrowing_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    borrowed_at = Column(DateTime(timezone=True), default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(BorrowingStatus), default=BorrowingStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    book = relationship("Book", backref="borrowing_records")
    user = relationship("User", backref="borrowing_records")
