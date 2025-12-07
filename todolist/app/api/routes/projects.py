from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todolist.app.api.dependencies import get_db
from todolist.app.api.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from todolist.app.services.project_service import ProjectService
from todolist.app.exceptions.errors import ProjectNotFoundError, DuplicateNameError

router = APIRouter(
    prefix="/api/projects",
    tags=["projects"],
)


@router.get("/", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRead]:
    """Retrieves a list of all projects.

    :param db: Database session dependency.
    :return: A list of ProjectRead schemas. Returns 200 OK with an empty list [] if no projects exist.
    """
    service = ProjectService(db)
    projects = service.list_projects()
    return [ProjectRead.model_validate(p) for p in projects]


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
        payload: ProjectCreate,
        db: Session = Depends(get_db),
) -> ProjectRead:
    """Creates a new project.

    Validates name uniqueness and schema constraints.
    :param payload: Data for the new project (name, description).
    :param db: Database session dependency.
    :return: The created ProjectRead schema.
    :raises HTTPException 409: If project name already exists (DuplicateNameError).
    """
    service = ProjectService(db)
    try:
        project = service.create_project(
            name=payload.name,
            description=payload.description or "",
        )
    except DuplicateNameError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
        project_id: int,
        payload: ProjectUpdate,
        db: Session = Depends(get_db),
) -> ProjectRead:
    """Updates one or more fields of an existing project (partial update).

    :param project_id: ID of the project to update.
    :param payload: Data for fields to update (name, description).
    :param db: Database session dependency.
    :return: The updated ProjectRead schema.
    :raises HTTPException 404: If the project is not found (ProjectNotFoundError).
    :raises HTTPException 409: If the new name already exists (DuplicateNameError).
    """
    service = ProjectService(db)
    try:
        project = service.update_project(
            project_id=project_id,
            name=payload.name,
            description=payload.description,
        )
    except ProjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    except DuplicateNameError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ProjectRead.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
        project_id: int,
        db: Session = Depends(get_db),
) -> None:
    """Deletes a project and all its associated tasks (Cascade Delete).

    :param project_id: ID of the project to delete.
    :param db: Database session dependency.
    :raises HTTPException 404: If the project is not found.
    """
    service = ProjectService(db)
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    service.delete_project(project_id)