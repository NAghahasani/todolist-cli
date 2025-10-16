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
# Base Manager (for inheritance)
# ---------------------------------------------------------------------------

class BaseManager:
    """Base class providing common CRUD operations for managers."""

    def __init__(self) -> None:
        self._items: List = []

    def list_all(self) -> List:
        """Return all managed items."""
        return self._items

    def _find_by_name(self, name: str):
        """Find an item by its name (case-insensitive)."""
        return next((item for item in self._items if item.name.lower() == name.strip().lower()), None)

    def delete_by_name(self, name: str) -> None:
        """Delete an item by name."""
        item = self._find_by_name(name)
        if not item:
            raise ValidationError(f"Item '{name}' not found.")
        self._items.remove(item)


# ---------------------------------------------------------------------------
# Application Logic
# ---------------------------------------------------------------------------

class ToDoApp(BaseManager):
    """In-memory application state and operations."""

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        super().__init__()
        self._max_projects = max_projects
        self._max_tasks = max_tasks

    def run(self) -> None:
        """Run the CLI main loop for managing projects."""
        print("📝 ToDoList CLI — Commands: new, edit, delete, list, exit.")

        while True:
            command = input("\n> ").strip().lower()

            if not command:
                continue

            if command in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            if command == "new":
                self._handle_new_project()
                continue

            if command == "edit":
                self._handle_edit_project()
                continue

            if command == "delete":
                self._handle_delete_project()
                continue

            if command == "list":
                self._handle_list_projects()
                continue

            print("⚠️ Unknown command. Try 'new', 'edit', 'delete', 'list', or 'exit'.")

    # ------------------------------- Handlers --------------------------------

    def _handle_new_project(self) -> None:
        """Handle creating a new project via CLI input."""
        name = input("Project name: ").strip()
        description = input("Description (optional): ").strip()

        try:
            project = self.create_project(name, description)
            print(f"✅ Project '{project.name}' created successfully!")
            print(f"Total projects: {len(self._items)}\n")
        except ValidationError as err:
            print(f"❌ {err}\n")

    def _handle_edit_project(self) -> None:
        """Handle editing an existing project via CLI input."""
        old_name = input("Enter current project name: ").strip()
        new_name = input("Enter new project name: ").strip()
        new_description = input("New description (optional): ").strip()

        try:
            project = self.edit_project(old_name, new_name, new_description)
            print(f"✏️ Project '{old_name}' updated successfully → '{project.name}'")
        except ValidationError as err:
            print(f"❌ {err}\n")

    def _handle_delete_project(self) -> None:
        """Handle deleting an existing project via CLI input."""
        name = input("Enter project name to delete: ").strip()

        try:
            self.delete_project(name)
            print(f"🗑 Project '{name}' deleted successfully.")
        except ValidationError as err:
            print(f"❌ {err}\n")

    def _handle_list_projects(self) -> None:
        """Handle listing all projects in the system."""
        projects = self.list_projects()
        if not projects:
            print("📂 No projects found.")
            return

        print("\n📋 Projects:")
        for index, project in enumerate(projects, start=1):
            print(f"{index}. {project.name} — {project.description or '(no description)'} "
                  f"({len(project.tasks)} tasks)")
        print()

    # ------------------------------- Core Logic ------------------------------

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project with validation checks."""
        if len(self._items) >= self._max_projects:
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

        for project in self._items:
            if project.name.strip().lower() == name.strip().lower():
                raise ValidationError("Project name must be unique.")

        project = Project(name=name.strip(), description=description.strip())
        self._items.append(project)
        return project

    def edit_project(self, old_name: str, new_name: str, new_description: str = "") -> Project:
        """Edit an existing project's name and description."""
        project = self._find_by_name(old_name)
        if not project:
            raise ValidationError(f"Project '{old_name}' not found.")

        if _is_blank(new_name):
            raise ValidationError("New project name cannot be empty.")

        if not (NAME_MIN_LEN <= len(new_name) <= NAME_MAX_LEN):
            raise ValidationError(
                f"Project name must be between {NAME_MIN_LEN} and {NAME_MAX_LEN} characters."
            )

        for p in self._items:
            if p is not project and p.name.strip().lower() == new_name.strip().lower():
                raise ValidationError("Another project with this name already exists.")

        if len(new_description) > DESC_MAX_LEN:
            raise ValidationError(f"Description must be {DESC_MAX_LEN} characters or fewer.")

        project.name = new_name.strip()
        project.description = new_description.strip()
        return project

    def delete_project(self, name: str) -> None:
        """Delete a project and its associated tasks."""
        project = self._find_by_name(name)
        if not project:
            raise ValidationError(f"Project '{name}' not found.")
        self._items.remove(project)

    def list_projects(self) -> List[Project]:
        """Return a list of all projects."""
        return self._items

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
