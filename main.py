"""CLI ToDoList – Phase 1 (In-Memory, Single File)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional
from dotenv import load_dotenv
import os
import sys

# ---------------------------------------------------------------------------
# Domain Models
# ---------------------------------------------------------------------------

Status = Literal["todo", "doing", "done"]


@dataclass
class Task:
    """Represents a task within a project."""
    title: str
    description: str = ""
    status: Status = "todo"


@dataclass
class Project:
    """Represents a project that groups tasks."""
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------------

class AppError(Exception):
    """Base error for the application."""


class ValidationError(AppError):
    """Raised when input validation fails."""


# ---------------------------------------------------------------------------
# Validation Constants and Helpers
# ---------------------------------------------------------------------------

NAME_MIN_LEN = 1
NAME_MAX_LEN = 50
DESC_MAX_LEN = 200


def _is_blank(value: str) -> bool:
    """Return True if a string is empty or whitespace only."""
    return not value or not value.strip()


# ---------------------------------------------------------------------------
# Application Logic
# ---------------------------------------------------------------------------

class ToDoApp:
    """In-memory application state and operations."""

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        self._projects: List[Project] = []
        self._max_projects = max_projects
        self._max_tasks = max_tasks

    def run(self) -> None:
        """Run the CLI main loop for managing projects."""
        print("📝 ToDoList CLI — Type 'new' to create a project or 'exit' to quit.\n")

        while True:
            command = input("> ").strip().lower()

            if not command:
                continue

            if command in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            if command == "new":
                self._handle_new_project()
                continue

            print("⚠️ Unknown command. Try 'new' or 'exit'.")

    def _handle_new_project(self) -> None:
        """Handle creating a new project via CLI input."""
        name = input("Project name: ").strip()
        description = input("Description (optional): ").strip()

        try:
            project = self.create_project(name, description)
            print(f"✅ Project '{project.name}' created successfully!")
            print(f"Total projects: {len(self._projects)}\n")
        except ValidationError as err:
            print(f"❌ {err}\n")

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project with validation checks."""
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")

        if _is_blank(name):
            raise ValidationError("Project name is required.")

        if not (NAME_MIN_LEN <= len(name) <= NAME_MAX_LEN):
            raise ValidationError(
                f"Project name must be between {NAME_MIN_LEN} and {NAME_MAX_LEN} characters."
            )

        if len(description) > DESC_MAX_LEN:
            raise ValidationError(
                f"Description must be {DESC_MAX_LEN} characters or fewer."
            )

        for project in self._projects:
            if project.name.strip().lower() == name.strip().lower():
                raise ValidationError("Project name must be unique.")

        project = Project(name=name.strip(), description=description.strip())
        self._projects.append(project)
        return project

    def edit_project(self, old_name: str, new_name: str, new_description: str = "") -> Project:
        """Edit an existing project's name and description."""
        # Find project by old name
        project = next((p for p in self._projects if p.name.lower() == old_name.strip().lower()), None)
        if not project:
            raise ValidationError(f"Project '{old_name}' not found.")

        # Validate new name
        if _is_blank(new_name):
            raise ValidationError("New project name cannot be empty.")

        if not (NAME_MIN_LEN <= len(new_name) <= NAME_MAX_LEN):
            raise ValidationError(
                f"Project name must be between {NAME_MIN_LEN} and {NAME_MAX_LEN} characters."
            )

        # Ensure uniqueness of new name
        for p in self._projects:
            if p is not project and p.name.strip().lower() == new_name.strip().lower():
                raise ValidationError("Another project with this name already exists.")

        # Validate description
        if len(new_description) > DESC_MAX_LEN:
            raise ValidationError(f"Description must be {DESC_MAX_LEN} characters or fewer.")

        # Apply edits
        project.name = new_name.strip()
        project.description = new_description.strip()
        return project

    @staticmethod
    def from_env() -> ToDoApp:
        """Factory that builds app from environment variables."""
        load_dotenv()
        try:
            max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
            max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
        except ValueError as exc:
            raise ValidationError("Environment values must be integers.") from exc
        return ToDoApp(max_projects=max_projects, max_tasks=max_tasks)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point function."""
    _ = argv or sys.argv[1:]
    app = ToDoApp.from_env()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
