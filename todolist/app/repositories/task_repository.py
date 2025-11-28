from typing import Optional

from sqlalchemy.orm import Session

from todolist.app.models import Task, Status


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_project(self, project_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def create(
        self,
        project_id: int,
        title: str,
        description: str | None = None,
        deadline=None,
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_status(self, task_id: int, new_status: Status) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            return None
        task.status = new_status
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True
