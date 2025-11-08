from sqlalchemy.orm import Session
from todolist.app.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Project).all()

    def get_by_id(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Project).filter(Project.name == name).first()

    def create(self, name: str):
        project = Project(name=name)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int):
        project = self.get_by_id(project_id)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False
