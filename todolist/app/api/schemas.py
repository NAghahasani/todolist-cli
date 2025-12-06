from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    status: str = Field(default="TODO")
    deadline: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    project_id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    deadline: datetime | None = None

    class Config:
        from_attributes = True