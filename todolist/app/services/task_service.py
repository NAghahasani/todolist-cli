from typing import Optional

from sqlalchemy.orm import Session

from todolist.app.models import Task, Status
from todolist.app.repositories.task_repository import TaskRepository
from todolist.app.repositories.project_repository import ProjectRepository


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)

    def list_tasks(self, project_id: int) -> list[Task]:
        # Ensure project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} does not exist")
        return self.repo.get_by_project(project_id)

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str | None = None,
        deadline=None,
    ) -> Task:
        # Check project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} does not exist")

        return self.repo.create(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )

    def update_status(self, task_id: int, new_status: Status) -> Optional[Task]:
        return self.repo.update_status(task_id, new_status)

    def delete_task(self, task_id: int) -> bool:
        return self.repo.delete(task_id)
