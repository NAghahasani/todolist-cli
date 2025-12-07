from sqlalchemy.orm import Session
from todolist.app.models import Project


class ProjectRepository:
    """Provides data access methods for the Project entity."""

    def __init__(self, db: Session):
        """Initializes the repository with a database session. [cite: 238, 247]"""
        self.db = db

    def get_all(self) -> list[Project]:
        """Returns a list of all projects in the database.

        :return: List of Project objects.
        """
        return self.db.query(Project).all()

    def get_by_id(self, project_id: int) -> Project | None:
        """Finds a project by its ID.

        :param project_id: The ID of the project.
        :return: Project object or None if not found.
        """
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_by_name(self, name: str) -> Project | None:
        """Finds a project by its unique name.

        :param name: The name of the project.
        :return: Project object or None if not found.
        """
        return self.db.query(Project).filter(Project.name == name).first()

    def create(self, name: str, description: str = "") -> Project:
        """Creates and persists a new project in the database.

        :param name: The name of the project.
        :param description: The description of the project.
        :return: The created Project instance.
        :raises Exception: If a database error occurs.
        """
        project = Project(name=name, description=description)
        try:
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            return project
        except Exception:
            self.db.rollback()
            raise

    def delete(self, project_id: int) -> bool:
        """Deletes a project by ID, including its related tasks (Cascade).

        :param project_id: The ID of the project to delete.
        :return: True if the project was deleted, False otherwise.
        :raises Exception: If a database error occurs during deletion.
        """
        project = self.get_by_id(project_id)
        if project:
            try:
                self.db.delete(project)
                self.db.commit()
                return True
            except Exception:
                self.db.rollback()
                raise
        return False