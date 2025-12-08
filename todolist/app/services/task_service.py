from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session
from todolist.app.persistence.models import Task
from todolist.app.persistence.models import status_enum
from todolist.app.persistence.repositories.task_repository import TaskRepository
from todolist.app.exceptions.errors import TaskNotFoundError

# The assumption is that status_enum.enums contains ('TODO', 'DOING', 'DONE') in uppercase.
ALLOWED_STATUSES = [e for e in status_enum.enums]


class TaskService:
    """Handles business logic for task creation, retrieval, modification, and status updates."""

    def __init__(self, db: Session) -> None:
        """Initializes the service with a TaskRepository instance."""
        self.repo = TaskRepository(db)
        self.db = db

    def list_tasks(self, project_id: int) -> list[Task]:
        """Returns all tasks for a specific project ID."""
        return self.repo.get_all(project_id)

    def get_task(self, project_id: int, task_id: int) -> Task | None:
        """Retrieves a single task by its IDs."""
        return self.repo.get_by_id(project_id, task_id)

    def create_task(
            self,
            project_id: int,
            title: str,
            description: str = "",
            status: str = "TODO",
            deadline: datetime | None = None,
    ) -> Task:


        return self.repo.create(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )

    def update_task(
            self,
            project_id: int,
            task_id: int,
            title: str | None = None,
            description: str | None = None,
            status: str | None = None,
            deadline: datetime | None = None,
    ) -> Task:
        """Updates task details using partial data (for PATCH)."""
        update_data = {
            "title": title,
            "description": description,
            "status": status,
            "deadline": deadline,
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if "status" in update_data:
            # FIX: Ensure status input is converted to uppercase before validation
            update_data["status"] = update_data["status"].upper()
            if update_data["status"] not in ALLOWED_STATUSES:
                raise ValueError("Invalid status value.")

        task = self.repo.update_by_data(
            project_id=project_id,
            task_id=task_id,
            data=update_data
        )

        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
        return task

    def update_task_status(
            self, project_id: int, task_id: int, new_status: str
    ) -> Task:
        """Updates only the status of a specific task."""

        # FIX: Ensure status input is converted to uppercase before validation
        new_status = new_status.upper()

        if new_status not in ALLOWED_STATUSES:
            raise ValueError("Invalid status value.")

        task = self.repo.update_by_data(
            project_id=project_id, task_id=task_id, data={"status": new_status}
        )
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
        return task

    def delete_task(self, project_id: int, task_id: int) -> bool:
        """Deletes a task by its ID."""
        task = self.repo.get_by_id(project_id, task_id)
        if task is None:
            return False

        return self.repo.delete(task_id)