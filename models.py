from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class PriorityEnum(str, enum.Enum):
    low    = "low"
    medium = "medium"
    high   = "high"

class StatusEnum(str, enum.Enum):
    pending     = "pending"
    in_progress = "in_progress"
    completed   = "completed"

class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    priority    = Column(Enum(PriorityEnum), default=PriorityEnum.medium)
    status      = Column(Enum(StatusEnum), default=StatusEnum.pending)
    completed   = Column(Boolean, default=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())
