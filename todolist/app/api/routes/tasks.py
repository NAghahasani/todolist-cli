from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todolist.app.api.dependencies import get_db
from todolist.app.api.schemas import TaskCreate, TaskRead
from todolist.app.services.project_service import ProjectService
from todolist.app.services.task_service import TaskService

router = APIRouter(
    prefix="/api/projects/{project_id}/tasks",
    tags=["tasks"],
)


@router.get("/", response_model=list[TaskRead])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
) -> list[TaskRead]:
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    task_svc = TaskService(db)
    tasks = task_svc.list_tasks(project_id)
    return [TaskRead.model_validate(t) for t in tasks]


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskRead:
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    task_svc = TaskService(db)
    try:
        task = task_svc.create_task(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            deadline=payload.deadline,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return TaskRead.model_validate(task)
