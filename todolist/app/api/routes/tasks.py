from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todolist.app.api.dependencies import get_db
from todolist.app.api.schemas import TaskCreate, TaskRead
from todolist.app.services.task_service import TaskService
from todolist.app.services.project_service import ProjectService

router = APIRouter(
    prefix="/api/projects/{project_id}/tasks",
    tags=["tasks"],
)


@router.get("/", response_model=list[TaskRead])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
):
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    task_svc = TaskService(db)
    tasks = task_svc.list_tasks(project_id)
    return [TaskRead.model_validate(t) for t in tasks]
