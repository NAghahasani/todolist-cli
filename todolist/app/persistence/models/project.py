from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from todolist.app.persistence.db import Base


class Project(Base):
    """SQLAlchemy model representing a project.

    Includes cascade rule to delete associated tasks upon project deletion.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, unique=True)
    description = Column(String(150), nullable=True)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")