from sqlalchemy.orm import Session
from todolist.app.models import Task


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
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(
        self,
        project_id: int,
        task_id: int,
        title: str | None,
        description: str | None,
        status: str | None,
        deadline: str | None,
    ) -> Task | None:
        task = self.db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()

        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if deadline is not None:
            task.deadline = deadline

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        deleted = self.db.query(Task).filter(Task.id == task_id).delete()
        self.db.commit()
        return deleted > 0