from sqlalchemy.orm import Session
from todolist.app.repositories.task_repository import TaskRepository
from todolist.app.models.task import Task

class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def list_tasks(self) -> list[Task]:
        return self.repo.get_all()

    def list_by_project(self, project_id: int) -> list[Task]:
        return self.repo.get_by_project(project_id)

    def get_task(self, task_id: int) -> Task | None:
        return self.repo.get_by_id(task_id)

    def create_task(
        self, project_id: int, title: str, description: str | None = None, due_date=None
    ) -> Task:
        return self.repo.create(project_id, title, description, due_date)

    def update_task_status(self, task_id: int, new_status: str) -> Task | None:
        return self.repo.update_status(task_id, new_status)

    def delete_task(self, task_id: int) -> bool:
        return self.repo.delete(task_id)
