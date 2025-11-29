from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todolist.app.api.dependencies import get_db
from todolist.app.api.schemas import ProjectRead
from todolist.app.services.project_service import ProjectService

router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
)


@router.get("/", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRead]:
    """Return all projects."""
    service = ProjectService(db)
    projects = service.list_projects()
    return [
        ProjectRead(id=p.id, name=p.name, description=p.description)
        for p in projects
    ]
