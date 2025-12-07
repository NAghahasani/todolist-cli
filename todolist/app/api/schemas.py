from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Project Schemas ---

class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    description: Optional[str] = Field(default=None, max_length=150)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=30)
    description: Optional[str] = Field(default=None, max_length=150)


class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True


# --- Task Schemas ---

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    description: Optional[str] = Field(default=None, max_length=150)
    status: str = Field(default="TODO")
    deadline: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    """Schema for reading a task, including read-only fields and closed_at."""
    id: int
    project_id: int
    created_at: Optional[datetime] = None
    # --- ADDED: closed_at for auto-close functionality verification ---
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=30)
    description: Optional[str] = Field(default=None, max_length=150)
    status: Optional[str] = None
    deadline: Optional[datetime] = None

    class Config:
        from_attributes = True