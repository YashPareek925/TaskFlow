from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models import PriorityEnum, StatusEnum

# ── Request Schemas ───────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title       : str            = Field(..., min_length=1, max_length=100, example="Buy groceries")
    description : Optional[str] = Field(None, max_length=500,              example="Milk, eggs, bread")
    priority    : Optional[PriorityEnum] = Field(PriorityEnum.medium,      example="high")
    status      : Optional[StatusEnum]   = Field(StatusEnum.pending,       example="pending")

class TaskUpdate(BaseModel):
    title       : Optional[str]          = Field(None, min_length=1, max_length=100)
    description : Optional[str]          = Field(None, max_length=500)
    priority    : Optional[PriorityEnum] = None
    status      : Optional[StatusEnum]   = None
    completed   : Optional[bool]         = None

# ── Response Schemas ──────────────────────────────────────────────────────────

class TaskResponse(BaseModel):
    id          : int
    title       : str
    description : Optional[str]
    priority    : PriorityEnum
    status      : StatusEnum
    completed   : bool
    created_at  : datetime
    updated_at  : Optional[datetime]

    class Config:
        from_attributes = True
