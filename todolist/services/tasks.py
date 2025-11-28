from typing import List
from todolist.models.task import Task
from todolist.repositories.task_repository import TaskRepository
from todolist.repositories.project_repository import ProjectRepository
from todolist.schemas.task import TaskCreate, TaskRead, TaskUpdateStatus

class TaskService:
    @staticmethod
    async def create_task(task: TaskCreate) -> TaskRead:
        db_task = await TaskRepository.create(task)
        return TaskRead.from_orm(db_task)

    @staticmethod
    async def list_tasks() -> List[TaskRead]:
        tasks = await TaskRepository.get_all()
        return [TaskRead.from_orm(task) for task in tasks]

    @staticmethod
    async def get_task(task_id: int) -> TaskRead:
        task = await TaskRepository.get_by_id(task_id)
        if task:
            return TaskRead.from_orm(task)
        return None

    @staticmethod
    async def update_task_status(task_id: int, task_status: TaskUpdateStatus) -> TaskRead:
        task = await TaskRepository.get_by_id(task_id)
        if not task:
            return None
        updated_task = await TaskRepository.update_status(task_id, task_status.status)
        return TaskRead.from_orm(updated_task)
