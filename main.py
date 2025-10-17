"""CLI ToDoList – Phase 1 (In-Memory, Single File)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Literal, Optional
from dotenv import load_dotenv
import os
import sys
import itertools
from datetime import datetime

Status = Literal["todo", "doing", "done"]

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Error Classes
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Core Application
# ---------------------------------------------------------------------------

class ToDoApp:
    """In-memory application state and operations."""

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        self._projects: List[Project] = []
        self._max_projects = max_projects
        self._max_tasks = max_tasks
        self._project_id_counter = itertools.count(1)
        self._task_id_counter = itertools.count(1)

    # -----------------------------------------------------------------------
    # PROJECT MANAGEMENT
    # -----------------------------------------------------------------------

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")
        if ValidationError._is_blank(name):
            raise ValidationError("Project name is required.")
        if not (ValidationError.NAME_MIN_LEN <= len(name) <= ValidationError.NAME_MAX_LEN):
            raise ValidationError("Invalid project name length.")
        for project in self._projects:
            if project.name.strip().lower() == name.strip().lower():
                raise ValidationError("Project name must be unique.")

        project = Project(
            id=next(self._project_id_counter),
            name=name.strip(),
            description=description.strip(),
        )
        self._projects.append(project)
        return project

    def find_project(self, name_or_id: str) -> Optional[Project]:
        for project in self._projects:
            if str(project.id) == str(name_or_id) or project.name.lower() == name_or_id.lower():
                return project
        return None

    # -----------------------------------------------------------------------
    # TASK MANAGEMENT
    # -----------------------------------------------------------------------

    def list_tasks(self, project_identifier: str) -> List[Task]:
        """Return all tasks for a specific project."""
        project = self.find_project(project_identifier)
        if not project:
            raise ValidationError(f"Project '{project_identifier}' not found.")
        if not project.tasks:
            raise ValidationError(f"No tasks found in project '{project.name}'.")
        # مرتب‌سازی براساس زمان ساخت
        return sorted(project.tasks, key=lambda t: t.created_at)

    # -----------------------------------------------------------------------
    # CLI Interface
    # -----------------------------------------------------------------------

    def run(self) -> None:
        """Run the CLI main loop for managing projects."""
        print("📝 ToDoList CLI — Commands: new, list, tasks, exit")

        while True:
            command = input("\n> ").strip().lower()

            if command in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            if command == "new":
                name = input("Project name: ").strip()
                description = input("Description (optional): ").strip()
                try:
                    project = self.create_project(name, description)
                    print(f"✅ Project '{project.name}' created successfully! (ID: {project.id})")
                except ValidationError as err:
                    print(f"❌ {err}")
                continue

            if command == "tasks":
                identifier = input("Enter project name or ID: ").strip()
                try:
                    tasks = self.list_tasks(identifier)
                    print(f"\n📋 Tasks in project '{identifier}':")
                    for task in tasks:
                        print(f"  [{task.id}] {task.title} — {task.status} ({task.created_at.strftime('%Y-%m-%d %H:%M')})")
                except ValidationError as err:
                    print(f"⚠️ {err}")
                continue

            print("⚠️ Unknown command. Try 'new', 'tasks', or 'exit'.")

    # -----------------------------------------------------------------------
    # ENV CONFIG
    # -----------------------------------------------------------------------

    @staticmethod
    def from_env() -> "ToDoApp":
        load_dotenv()
        try:
            max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
            max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
        except ValueError as exc:
            raise ValidationError("Environment values must be integers.") from exc
        return ToDoApp(max_projects=max_projects, max_tasks=max_tasks)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    _ = argv or sys.argv[1:]
    app = ToDoApp.from_env()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
