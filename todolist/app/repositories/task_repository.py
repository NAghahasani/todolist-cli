from sqlalchemy.orm import Session
from todolist.app.models.task import Task

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_project(self, project_id: int):
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def create(self, project_id: int, title: str, description: str = None, due_date=None):
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            due_date=due_date,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_status(self, task_id: int, new_status: str):
        task = self.get_by_id(task_id)
        if task:
            task.status = new_status
            self.db.commit()
            self.db.refresh(task)
            return task
        return None

    def delete(self, task_id: int):
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False
