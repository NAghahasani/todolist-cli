from sqlalchemy.orm import Session
from todolist.app import ProjectRepository
from todolist.app.models.project import Project

class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def list_projects(self) -> list[Project]:
        return self.repo.get_all()

    def get_project(self, project_id: int) -> Project | None:
        return self.repo.get_by_id(project_id)

    def create_project(self, name: str) -> Project:
        existing = self.repo.get_by_name(name)
        if existing:
            raise ValueError("Project with this name already exists")
        return self.repo.create(name)

    def delete_project(self, project_id: int) -> bool:
        return self.repo.delete(project_id)
