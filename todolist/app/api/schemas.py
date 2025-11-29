from __future__ import annotations

from pydantic import BaseModel


class ProjectRead(BaseModel):
    """Read model for Project entity returned by the API."""
    id: int
    name: str
    description: str | None = None
