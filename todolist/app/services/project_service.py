from __future__ import annotations

from sqlalchemy.orm import Session

from todolist.app.models import Project
from todolist.app.repositories.project_repository import ProjectRepository
from todolist.app.exceptions.errors import ProjectNotFoundError, DuplicateNameError


class ProjectService:
    """Handles business logic for project creation, retrieval, and modification."""

    def __init__(self, db: Session) -> None:
        """Initializes the service with a ProjectRepository instance.

        :param db: The SQLAlchemy database session.
        """
        self.repo = ProjectRepository(db)
        self.db = db

    def list_projects(self) -> list[Project]:
        """Returns a list of all projects in the database.

        :return: List of Project objects.
        """
        return self.repo.get_all()

    def get_project(self, project_id: int) -> Project | None:
        """Retrieves a single project by ID.

        :param project_id: The ID of the project.
        :return: Project object or None.
        """
        return self.repo.get_by_id(project_id)

    def create_project(self, name: str, description: str = "") -> Project:
        """Creates a new project, ensuring the name is unique.

        :param name: The unique name of the project (max 30 chars).
        :param description: Project description (max 150 chars).
        :return: The created Project instance.
        :raises DuplicateNameError: If a project with the same name already exists.
        """
        existing = self.repo.get_by_name(name)
        if existing:
            raise DuplicateNameError("Project with this name already exists")

        # Repository handles transactional safety for creation
        return self.repo.create(name=name, description=description)

    def update_project(self, project_id: int, name: str | None = None, description: str | None = None) -> Project:
        """Updates project details (name and/or description).

        :param project_id: ID of the project to update.
        :param name: New unique name for the project (optional).
        :param description: New description for the project (optional).
        :return: The updated Project instance.
        :raises ProjectNotFoundError: If the project ID does not exist.
        :raises DuplicateNameError: If the new name is already in use by another project.
        """
        project = self.repo.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        if name is not None:
            existing = self.repo.get_by_name(name)
            if existing and existing.id != project_id:
                raise DuplicateNameError("Project with this name already exists")
            project.name = name

        if description is not None:
            project.description = description

        try:
            self.db.commit()
            self.db.refresh(project)
            return project
        except Exception:
            self.db.rollback()
            raise

    def delete_project(self, project_id: int) -> bool:
        """Deletes a project and cascades deletion to all associated tasks.

        :param project_id: ID of the project to delete.
        :return: True if the project was deleted, False otherwise.
        """
        return self.repo.delete(project_id)