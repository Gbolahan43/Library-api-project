import uuid
import enum
from sqlalchemy import Column, DateTime, ForeignKey, Enum, Numeric, Text, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class FineStatus(str, enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"
    WAIVED = "Waived"
    OVERDUE = "Overdue"

class Fine(Base):
    __tablename__ = "fines"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    borrowing_id = Column(Uuid(as_uuid=True), ForeignKey("borrowing_records.id"), nullable=False)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    fine_date = Column(DateTime(timezone=True), default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(FineStatus), default=FineStatus.PENDING)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    borrowing_record = relationship("BorrowingRecord", backref="fines")
    user = relationship("User", backref="fines")
