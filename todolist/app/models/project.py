from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from todolist.app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
