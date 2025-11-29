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
        raise HTTPException(status_code=404, detail="Project not found")

    task_svc = TaskService(db)
    tasks = task_svc.list_tasks(project_id)
    return [TaskRead.model_validate(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskRead:
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    task_svc = TaskService(db)
    task = task_svc.get_task(project_id, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskRead.model_validate(task)


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskRead:
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

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
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return TaskRead.model_validate(task)


@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status(
    project_id: int,
    task_id: int,
    status_value: str,
    db: Session = Depends(get_db),
) -> TaskRead:
    project_svc = ProjectService(db)

    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    task_svc = TaskService(db)
    try:
        task = task_svc.update_task_status(
            project_id=project_id,
            task_id=task_id,
            new_status=status_value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    task_svc = TaskService(db)
    if not task_svc.get_task(project_id, task_id):
        raise HTTPException(status_code=404, detail="Task not found")

    task_svc.delete_task(project_id, task_id)
