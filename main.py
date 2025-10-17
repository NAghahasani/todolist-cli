"""CLI ToDoList – Phase 1 (In-Memory, Single File)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
import itertools

Status = Literal["todo", "doing", "done"]


@dataclass
class Task:
    """Represents a task within a project."""
    id: int
    title: str
    description: str = ""
    status: Status = "todo"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Project:
    """Represents a project that groups tasks."""
    id: int
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


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


class ToDoApp:
    """In-memory application state and operations."""

    _project_id_counter = itertools.count(1)
    _task_id_counter = itertools.count(1)

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        self._projects: List[Project] = []
        self._max_projects = max_projects
        self._max_tasks = max_tasks

    # --------------------------- PROJECT MANAGEMENT --------------------------

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project with validation checks."""
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")
        if ValidationError._is_blank(name):
            raise ValidationError("Project name is required.")
        if not (ValidationError.NAME_MIN_LEN <= len(name) <= ValidationError.NAME_MAX_LEN):
            raise ValidationError("Invalid project name length.")
        if len(description) > ValidationError.DESC_MAX_LEN:
            raise ValidationError("Description too long.")
        if any(p.name.lower() == name.lower() for p in self._projects):
            raise ValidationError("Project name must be unique.")

        project = Project(
            id=next(self._project_id_counter),
            name=name.strip(),
            description=description.strip(),
        )
        self._projects.append(project)
        self._projects.sort(key=lambda p: p.created_at)
        return project

    def list_projects(self) -> List[Project]:
        """Return all projects sorted by creation time."""
        return sorted(self._projects, key=lambda p: p.created_at)


# ---------------------------------------------------------------------------
# CLI Runner
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point function."""
    load_dotenv()
    _ = argv or sys.argv[1:]

    max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
    max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
    app = ToDoApp(max_projects, max_tasks)

    print("📝 ToDoList CLI — Type 'new' to create a project, 'list' to view projects, or 'exit' to quit.")
    while True:
        command = input("\n> ").strip().lower()
        if command in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        if command == "new":
            name = input("Project name: ").strip()
            description = input("Description (optional): ").strip()
            try:
                project = app.create_project(name, description)
                print(f"✅ Project created: [ID={project.id}] {project.name}")
            except ValidationError as e:
                print(f"❌ {e}")
            continue

        if command == "list":
            projects = app.list_projects()
            if not projects:
                print("⚠️ No projects found.")
            else:
                print("\n📋 Projects:")
                for p in projects:
                    print(f"  ID={p.id} | Name='{p.name}' | Description='{p.description}' | Created={p.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            continue

        print("⚠️ Unknown command. Try 'new', 'list', or 'exit'.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
