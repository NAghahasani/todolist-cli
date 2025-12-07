from sqlalchemy.orm import Session
from todolist.app.models import Task
from todolist.app.models.task import status_enum


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, project_id: int, task_id: int) -> Task | None:
        return (
            self.db.query(Task)
            .filter(Task.id == task_id, Task.project_id == project_id)
            .first()
        )

    def get_all(self, project_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def create(
        self,
        project_id: int,
        title: str,
        description: str,
        status: str,
        deadline: str | None = None,
    ) -> Task:
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
        """Updates a task using a dictionary of data with transactional safety."""
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
        try:
            deleted = self.db.query(Task).filter(Task.id == task_id).delete()
            self.db.commit()
            return deleted > 0
        except Exception:
            self.db.rollback()
            raise