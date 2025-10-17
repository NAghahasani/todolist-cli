"""CLI ToDoList – Add Task Feature (Phase 2)."""
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
        project = self._find_by_name(name)
        if not project:
            raise ValidationError(f"Project '{name}' not found.")
        self._projects.remove(project)

    def edit_project(self, old_name: str, new_name: str, new_description: str = "") -> Project:
        project = self._find_by_name(old_name)
        if not project:
            raise ValidationError(f"Project '{old_name}' not found.")
        if ValidationError._is_blank(new_name):
            raise ValidationError("New project name cannot be empty.")
        project.name = new_name.strip()
        project.description = new_description.strip()
        return project

    def list_projects(self) -> List[Project]:
        return self._projects

    # --------------------- TASK MANAGEMENT ---------------------

    def add_task(self, project_name: str, title: str, description: str = "") -> Task:
        """Add a new task to a specific project."""
        project = self._find_by_name(project_name)
        if not project:
            raise ValidationError(f"Project '{project_name}' not found.")
        if len(project.tasks) >= self._max_tasks:
            raise ValidationError("Task limit reached for this project.")
        if ValidationError._is_blank(title):
            raise ValidationError("Task title is required.")
        task = Task(title=title.strip(), description=description.strip())
        project.tasks.append(task)
        return task

    # --------------------- HELPERS ---------------------

    def _find_by_name(self, name: str) -> Optional[Project]:
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

    # --------------------- CLI ---------------------

    def run(self) -> None:
        print("📝 ToDoList CLI — Commands: new, edit, delete, list, add, exit.")
        while True:
            command = input("\n> ").strip().lower()
            if command in {"exit", "quit"}:
                print("👋 Goodbye!")
                break
            if command == "new":
                name = input("Project name: ").strip()
                desc = input("Description (optional): ").strip()
                try:
                    p = self.create_project(name, desc)
                    print(f"✅ Project '{p.name}' created successfully!")
                except ValidationError as e:
                    print(f"❌ {e}")
            elif command == "add":
                proj = input("Project name: ").strip()
                title = input("Task title: ").strip()
                desc = input("Description (optional): ").strip()
                try:
                    t = self.add_task(proj, title, desc)
                    print(f"🆕 Task '{t.title}' added to project '{proj}'")
                except ValidationError as e:
                    print(f"❌ {e}")
            elif command == "list":
                projects = self.list_projects()
                if not projects:
                    print("📂 No projects found.")
                    continue
                print("\n📋 Projects:")
                for i, p in enumerate(projects, start=1):
                    print(f"{i}. {p.name} — {p.description or 'No description'} ({len(p.tasks)} tasks)")
            else:
                print("⚠️ Unknown command.")


# -----------------------------------------------------------------------------
# Main Entry
# -----------------------------------------------------------------------------
def main(argv: Opسtional[List[str]] = None) -> int:
    _ = argv or sys.argv[1:]
    app = ToDoApp.from_env()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
