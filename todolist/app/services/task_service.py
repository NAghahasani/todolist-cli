from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session
from todolist.app.models import Task
from todolist.app.models.task import status_enum
from todolist.app.repositories.task_repository import TaskRepository


ALLOWED_STATUSES = [e for e in status_enum.enums]


class TaskService:
    def __init__(self, db: Session) -> None:
        self.repo = TaskRepository(db)
        self.db = db

    def list_tasks(self, project_id: int) -> list[Task]:
        return self.repo.get_all(project_id)

    def get_task(self, project_id: int, task_id: int) -> Task | None:
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

        # ساخت دیکشنری داده ها و حذف مقادیر None
        update_data = {
            "title": title,
            "description": description,
            "status": status,
            "deadline": deadline,
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}


        if "status" in update_data and update_data["status"] not in ALLOWED_STATUSES:
            raise ValueError("Invalid status value.")

        task = self.repo.update_by_data(
            project_id=project_id,
            task_id=task_id,
            data=update_data
        )

        if task is None:
            raise ValueError("Task not found")
        return task

    def update_task_status(
            self, project_id: int, task_id: int, new_status: str
    ) -> Task:

        if new_status not in ALLOWED_STATUSES:
            raise ValueError("Invalid status value.")

        task = self.repo.update_by_data(
            project_id=project_id, task_id=task_id, data={"status": new_status}
        )
        if task is None:
            raise ValueError("Task not found")
        return task

    def delete_task(self, project_id: int, task_id: int) -> bool:
        return self.repo.delete(task_id)