from fastapi import APIRouter, HTTPException, status
from typing import List

from todolist.schemas.task import TaskCreate, TaskRead, TaskUpdateStatus
from todolist.services.tasks import TaskService

router = APIRouter()

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    created_task = await TaskService.create_task(task)
    return created_task

@router.get("/", response_model=List[TaskRead])
async def list_tasks():
    return await TaskService.list_tasks()

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int):
    task = await TaskService.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.patch("/{task_id}/status", response_model=TaskRead)
async def update_task_status(task_id: int, task_status: TaskUpdateStatus):
    updated_task = await TaskService.update_task_status(task_id, task_status)
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task
