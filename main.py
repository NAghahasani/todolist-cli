"""CLI ToDoList – Feature: Delete Task (Core)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional
from dotenv import load_dotenv
import os
import sys


# -----------------------------------------------------------------------------
# Type Definitions
# -----------------------------------------------------------------------------
Status = Literal["todo", "doing", "done"]


# -----------------------------------------------------------------------------
# Data Models
# -----------------------------------------------------------------------------
@dataclass
class Task:
    title: str
    description: str = ""
    status: Status = "todo"


@dataclass
class Project:
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)


# -----------------------------------------------------------------------------
# Custom Exceptions
# -----------------------------------------------------------------------------
class AppError(Exception):
    """Base error for the application."""


class ValidationError(AppError):
    """Raised when input validation fails."""

    NAME_MIN_LEN = 1
    NAME_MAX_LEN = 50
    DESC_MAX_LEN = 200

    @staticmethod
    def _is_blank(value: str) -> bool:
        return not value or not value.strip()


# -----------------------------------------------------------------------------
# Core Application
# -----------------------------------------------------------------------------
class ToDoApp:
    """In-memory application state and operations."""

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        self._projects: List[Project] = []
        self._max_projects = max_projects
        self._max_tasks = max_tasks

    # --------------------- PROJECT MANAGEMENT ---------------------

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")
        if ValidationError._is_blank(name):
            raise ValidationError("Project name is required.")
        if not (ValidationError.NAME_MIN_LEN <= len(name) <= ValidationError.NAME_MAX_LEN):
            raise ValidationError("Invalid project name length.")
        for p in self._projects:
            if p.name.strip().lower() == name.strip().lower():
                raise ValidationError("Project name must be unique.")
        project = Project(name=name.strip(), description=description.strip())
        self._projects.append(project)
        return project

    def delete_project(self, name: str) -> None:
        """Deletes a project and all its associated tasks (Cascade Delete)."""
        project = self._find_project(name)
        if not project:
            raise ValidationError(f"Project '{name}' not found.")
        # Cascade delete
        project.tasks.clear()
        self._projects.remove(project)

    def list_projects(self) -> List[Project]:
        return self._projects

    # --------------------- TASK MANAGEMENT ---------------------

    def add_task(self, project_name: str, title: str, description: str = "") -> Task:
        project = self._find_project(project_name)
        if not project:
            raise ValidationError(f"Project '{project_name}' not found.")
        if len(project.tasks) >= self._max_tasks:
            raise ValidationError("Task limit reached for this project.")
        if ValidationError._is_blank(title):
            raise ValidationError("Task title is required.")
        task = Task(title=title.strip(), description=description.strip())
        project.tasks.append(task)
        return task

    def delete_task(self, project_name: str, task_title: str) -> None:
        """Deletes a task by title within a specific project."""
        project = self._find_project(project_name)
        if not project:
            raise ValidationError(f"Project '{project_name}' not found.")
        task = next((t for t in project.tasks if t.title.lower() == task_title.strip().lower()), None)
        if not task:
            raise ValidationError(f"Task '{task_title}' not found in project '{project_name}'.")
        project.tasks.remove(task)

    # --------------------- HELPERS ---------------------

    def _find_project(self, name: str) -> Optional[Project]:
        return next((p for p in self._projects if p.name.lower() == name.lower()), None)

    # --------------------- ENV FACTORY ---------------------

    @staticmethod
    def from_env() -> ToDoApp:
        load_dotenv()
        try:
            max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
            max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
        except ValueError as exc:
            raise ValidationError("Environment values must be integers.") from exc
        return ToDoApp(max_projects=max_projects, max_tasks=max_tasks)

    # --------------------- CLI (placeholder) ---------------------

    def run(self) -> None:
        print("📝 ToDoList CLI — Commands: new, add, delete-task, list, exit.")
        print("(CLI command for delete-task will be added in the next step.)")


# -----------------------------------------------------------------------------
# Main Entry
# -----------------------------------------------------------------------------
def main(argv: Optional[List[str]] = None) -> int:
    _ = argv or sys.argv[1:]
    app = ToDoApp.from_env()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
