from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from todolist.app.models import Task, Status
from todolist.app.repositories.task_repository import TaskRepository
from todolist.app.repositories.project_repository import ProjectRepository
from todolist.core.config import load_config


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.config = load_config()

    def list_tasks(self, project_id: int) -> list[Task]:
        return self.get_by_project(project_id)

    def get_by_project(self, project_id: int) -> list[Task]:
        try:
            # If repository has a dedicated method
            return self.repo.get_by_project(project_id)  # type: ignore[attr-defined]
        except AttributeError:
            # Fallback: query directly
            return (
                self.db.query(Task)
                .filter(Task.project_id == project_id)
                .order_by(Task.id.asc())
                .all()
            )

    def count_tasks(self, project_id: int) -> int:
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .count()
        )

    def create(
        self,
        project_id: int,
        title: str,
        description: str | None = None,
        deadline=None,
    ) -> Task:
        project = self.project_repo.get_by_id(project_id)
        if project is None:
            raise ValueError(f"Project {project_id} does not exist")

        if self.count_tasks(project_id) >= self.config.max_tasks:
            raise ValueError("Maximum number of tasks reached")

        task = self.repo.create(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        return task

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str | None = None,
        status: str = "TODO",
        deadline=None,
    ) -> Task:
        try:
            status_enum = Status(status)
        except ValueError:
            status_enum = Status.TODO

        task = self.create(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )

        task.status = status_enum
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.repo.get_by_id(task_id)

    def get_task(self, project_id: int, task_id: int) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if task is None or task.project_id != project_id:
            return None
        return task

    def update_task_status(self, task_id: int, new_status: Status) -> Optional[Task]:
        return self.repo.update_status(task_id, new_status)

    def delete(self, task_id: int) -> bool:
        return self.repo.delete(task_id)

    def delete_task(self, project_id: int, task_id: int) -> bool:
        task = self.get_task(project_id, task_id)
        if task is None:
            return False
        return self.repo.delete(task_id)
