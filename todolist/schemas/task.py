from pydantic import BaseModel
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None  # You can later parse this into datetime

class TaskRead(TaskCreate):
    id: int
    status: StatusEnum
    project_id: int

    class Config:
        orm_mode = True

class TaskUpdateStatus(BaseModel):
    status: StatusEnum
