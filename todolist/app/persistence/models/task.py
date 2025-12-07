from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from todolist.app.persistence.db import Base
from sqlalchemy.dialects.postgresql import ENUM

status_enum = ENUM("TODO", "IN_PROGRESS", "DONE", name="status")


class Task(Base):
    """SQLAlchemy model representing a task associated with a project."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(30), nullable=False)
    description = Column(String(150), nullable=True)
    status = Column(status_enum, default="TODO", nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)

    project = relationship("Project", back_populates="tasks")