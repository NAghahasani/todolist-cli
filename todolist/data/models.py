from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Literal, Optional

Status = Literal["todo", "doing", "done"]


@dataclass
class Task:
    """Data model for an in-memory task."""
    id: int
    title: str
    description: str = ""
    status: Status = "todo"
    deadline: Optional[str] = None


@dataclass
class Project:
    """Data model for an in-memory project containing multiple tasks."""
    id: int
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)
