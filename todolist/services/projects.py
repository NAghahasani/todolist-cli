from typing import List
from todolist.models.project import Project
from todolist.repositories.project_repository import ProjectRepository
from todolist.schemas.project import ProjectCreate, ProjectRead

class ProjectService:
    @staticmethod
    async def create_project(project: ProjectCreate) -> ProjectRead:
        db_project = await ProjectRepository.create(project)
        return ProjectRead.from_orm(db_project)

    @staticmethod
    async def list_projects() -> List[ProjectRead]:
        projects = await ProjectRepository.get_all()
        return [ProjectRead.from_orm(project) for project in projects]

    @staticmethod
    async def get_project(project_id: int) -> ProjectRead:
        project = await ProjectRepository.get_by_id(project_id)
        if project:
            return ProjectRead.from_orm(project)
        return None
