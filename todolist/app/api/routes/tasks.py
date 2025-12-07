from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import Custom Exceptions
from todolist.app.exceptions.errors import TaskNotFoundError, ProjectNotFoundError, MaxLimitExceededError

from todolist.app.api.dependencies import get_db
from todolist.app.api.schemas import TaskCreate, TaskRead, TaskUpdate
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
    """Retrieves all tasks for a specific project.

    :param project_id: ID of the parent project.
    :param db: Database session dependency.
    :raises HTTPException 404: If the project is not found.
    :return: List of TaskRead schemas.
    """
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

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
    """Creates a new task within a specific project.

    :param project_id: ID of the parent project.
    :param payload: Data for the new task.
    :param db: Database session dependency.
    :raises HTTPException 404: If the project is not found.
    :raises HTTPException 409: If max task limit is exceeded (MaxLimitExceededError).
    :raises HTTPException 400: If status or deadline is invalid (ValueError).
    :return: The created TaskRead schema.
    """
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    task_svc = TaskService(db)
    try:
        task = task_svc.create_task(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            deadline=payload.deadline,
        )
    except MaxLimitExceededError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
        project_id: int,
        task_id: int,
        payload: TaskUpdate,
        db: Session = Depends(get_db),
) -> TaskRead:
    """Updates one or more fields of an existing task.

    :param project_id: ID of the parent project.
    :param task_id: ID of the task to update.
    :param payload: Data for fields to update.
    :param db: Database session dependency.
    :raises HTTPException 404: If project or task is not found (TaskNotFoundError).
    :raises HTTPException 400: If status is invalid (ValueError).
    :return: The updated TaskRead schema.
    """
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    task_svc = TaskService(db)
    try:
        task = task_svc.update_task(
            project_id=project_id,
            task_id=task_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            deadline=payload.deadline,
        )
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return TaskRead.model_validate(task)


@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status(
        project_id: int,
        task_id: int,
        status_value: str,
        db: Session = Depends(get_db),
) -> TaskRead:
    """Updates only the status of an existing task.

    :param project_id: ID of the parent project.
    :param task_id: ID of the task to update.
    :param status_value: The new status string.
    :param db: Database session dependency.
    :raises HTTPException 404: If project or task is not found (TaskNotFoundError).
    :raises HTTPException 400: If status_value is invalid (ValueError).
    :return: The updated TaskRead schema.
    """
    project_svc = ProjectService(db)

    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    task_svc = TaskService(db)
    try:
        task = task_svc.update_task_status(
            project_id=project_id,
            task_id=task_id,
            new_status=status_value,
        )
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        project_id: int,
        task_id: int,
        db: Session = Depends(get_db),
) -> None:
    """Deletes a specific task.

    :param project_id: ID of the parent project.
    :param task_id: ID of the task to delete.
    :param db: Database session dependency.
    :raises HTTPException 404: If project or task is not found.
    """
    project_svc = ProjectService(db)
    if project_svc.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    task_svc = TaskService(db)

    # Check if task exists and is in the correct project scope
    if not task_svc.get_task(project_id, task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    task_svc.delete_task(project_id, task_id)