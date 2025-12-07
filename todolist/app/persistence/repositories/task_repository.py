from sqlalchemy.orm import Session
from todolist.app.persistence.models import Task


class TaskRepository:
    """Provides data access methods for the Task entity."""

    def __init__(self, db: Session) -> None:
        """Initializes the repository with a database session.

        :param db: The SQLAlchemy database session.
        """
        self.db = db

    def get_by_id(self, project_id: int, task_id: int) -> Task | None:
        """Finds a specific task by project ID and task ID.

        :param project_id: The ID of the parent project.
        :param task_id: The ID of the task.
        :return: Task object or None if not found.
        """
        return (
            self.db.query(Task)
            .filter(Task.id == task_id, Task.project_id == project_id)
            .first()
        )

    def get_all(self, project_id: int) -> list[Task]:
        """Returns a list of all tasks associated with a specific project.

        :param project_id: The ID of the parent project.
        :return: List of Task objects.
        """
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def create(
            self,
            project_id: int,
            title: str,
            description: str,
            status: str,
            deadline: str | None = None,
    ) -> Task:
        """Creates and persists a new task in the database.

        :param project_id: The ID of the parent project.
        :param title: The title of the task (max 30 chars).
        :param description: The description of the task (max 150 chars).
        :param status: The initial status of the task.
        :param deadline: Optional deadline (YYYY-MM-DD format).
        :return: The created Task instance.
        :raises Exception: If a database error occurs (transactional safety).
        """
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )
        try:
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception:
            self.db.rollback()
            raise

    def update_by_data(
            self,
            project_id: int,
            task_id: int,
            data: dict
    ) -> Task | None:
        """Updates a task using a dictionary of data with transactional safety (for PATCH requests).

        :param project_id: The ID of the parent project.
        :param task_id: The ID of the task to update.
        :param data: Dictionary containing fields to update (e.g., {'title': 'new title'}).
        :return: The updated Task object or None if the task was not found.
        :raises Exception: If a database error occurs during commit.
        """
        task = self.db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()

        if not task:
            return None

        for key, value in data.items():
            setattr(task, key, value)

        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception:
            self.db.rollback()
            raise

    def delete(self, task_id: int) -> bool:
        """Deletes a task by its ID.

        :param task_id: The ID of the task to delete.
        :return: True if the task was deleted, False otherwise.
        :raises Exception: If a database error occurs during deletion.
        """
        try:
            deleted = self.db.query(Task).filter(Task.id == task_id).delete()
            self.db.commit()
            return deleted > 0
        except Exception:
            self.db.rollback()
            raise