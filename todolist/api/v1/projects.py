from fastapi import APIRouter, HTTPException, status
from typing import List

from todolist.schemas.project import ProjectCreate, ProjectRead
from todolist.services.projects import ProjectService

router = APIRouter()

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    created_project = await ProjectService.create_project(project)
    return created_project

@router.get("/", response_model=List[ProjectRead])
async def list_projects():
    return await ProjectService.list_projects()

@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int):
    project = await ProjectService.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project
