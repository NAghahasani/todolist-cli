from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from todolist.app.db.base import Base
import enum


class Status(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(Status), default=Status.TODO, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status.name})>"
