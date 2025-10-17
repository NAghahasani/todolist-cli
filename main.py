"""CLI ToDoList – Full Refactored Version (All Features Integrated)"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional
from dotenv import load_dotenv
import os
import sys

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


@dataclass
class Project:
    """Represents a project that groups tasks."""
    id: int
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Errors and Validation
# ---------------------------------------------------------------------------
class AppError(Exception):
    """Base error for the application."""


class ValidationError(AppError):
    """Raised when input validation fails."""

    NAME_MIN_LEN = 1
    NAME_MAX_LEN = 50
    DESC_MAX_LEN = 200

    @staticmethod
    def is_blank(value: str) -> bool:
        return not value or not value.strip()


# ---------------------------------------------------------------------------
# Core Application Logic
# ---------------------------------------------------------------------------
class ToDoApp:
    """In-memory application state and operations."""

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        self._projects: List[Project] = []
        self._max_projects = max_projects
        self._max_tasks = max_tasks
        self._next_project_id = 1
        self._next_task_id = 1

    # --------------------------- PROJECT MANAGEMENT ------------------------

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")

        if ValidationError.is_blank(name):
            raise ValidationError("Project name is required.")

        if not (ValidationError.NAME_MIN_LEN <= len(name) <= ValidationError.NAME_MAX_LEN):
            raise ValidationError("Invalid project name length.")

        for p in self._projects:
            if p.name.strip().lower() == name.strip().lower():
                raise ValidationError("Project name must be unique.")

        project = Project(id=self._next_project_id, name=name.strip(), description=description.strip())
        self._projects.append(project)
        self._next_project_id += 1
        return project

    def edit_project(self, project_id: int, new_name: str, new_description: str = "") -> Project:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError(f"Project with ID={project_id} not found.")

        if ValidationError.is_blank(new_name):
            raise ValidationError("Project name cannot be empty.")

        project.name = new_name.strip()
        project.description = new_description.strip()
        return project

    def delete_project(self, project_id: int) -> None:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError(f"Project with ID={project_id} not found.")
        self._projects.remove(project)

    def list_projects(self) -> List[Project]:
        return sorted(self._projects, key=lambda p: p.id)

    # --------------------------- TASK MANAGEMENT --------------------------

    def add_task(self, project_id: int, title: str, description: str = "") -> Task:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError(f"Project ID={project_id} not found.")

        if len(project.tasks) >= self._max_tasks:
            raise ValidationError("Task limit reached for this project.")

        if ValidationError.is_blank(title):
            raise ValidationError("Task title is required.")

        task = Task(id=self._next_task_id, title=title.strip(), description=description.strip())
        self._next_task_id += 1
        project.tasks.append(task)
        return task

    def edit_task(self, project_id: int, task_id: int, new_title: str, new_description: str, new_status: Status) -> Task:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = self._find_task(project, task_id)
        if not task:
            raise ValidationError("Task not found.")

        task.title = new_title.strip()
        task.description = new_description.strip()
        if new_status not in ["todo", "doing", "done"]:
            raise ValidationError("Invalid status value.")
        task.status = new_status
        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = self._find_task(project, task_id)
        if not task:
            raise ValidationError("Task not found.")
        project.tasks.remove(task)

    def change_status(self, project_id: int, task_id: int, new_status: Status) -> Task:
        if new_status not in ["todo", "doing", "done"]:
            raise ValidationError("Invalid status.")

        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = self._find_task(project, task_id)
        if not task:
            raise ValidationError("Task not found.")

        task.status = new_status
        return task

    def list_tasks(self, project_id: int) -> List[Task]:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")
        return sorted(project.tasks, key=lambda t: t.id)

    # --------------------------- HELPERS ----------------------------------

    def _find_project(self, project_id: int) -> Optional[Project]:
        return next((p for p in self._projects if p.id == project_id), None)

    def _find_task(self, project: Project, task_id: int) -> Optional[Task]:
        return next((t for t in project.tasks if t.id == task_id), None)

    # --------------------------- FACTORY ----------------------------------

    @staticmethod
    def from_env() -> ToDoApp:
        load_dotenv()
        try:
            max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
            max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
        except ValueError as exc:
            raise ValidationError("Environment values must be integers.") from exc
        return ToDoApp(max_projects=max_projects, max_tasks=max_tasks)

    # --------------------------- CLI LOOP ---------------------------------

    def run(self) -> None:
        print("🧱 ToDoList CLI — Commands: new, list, edit, delete, add, edit-task, delete-task, status, tasks, exit")

        while True:
            command = input("\n> ").strip().lower()

            try:
                if command in {"exit", "quit"}:
                    print("👋 Goodbye!")
                    break

                elif command == "new":
                    name = input("Project name: ").strip()
                    desc = input("Description (optional): ").strip()
                    project = self.create_project(name, desc)
                    print(f"✅ Project '{project.name}' created (ID={project.id})")

                elif command == "list":
                    projects = self.list_projects()
                    if not projects:
                        print("⚠️ No projects found.")
                    else:
                        print("\n📋 Projects:")
                        for p in projects:
                            print(f"  [{p.id}] {p.name} — {p.description or 'No description'} ({len(p.tasks)} tasks)")

                elif command == "edit":
                    pid = int(input("Project ID: "))
                    new_name = input("New name: ").strip()
                    new_desc = input("New description: ").strip()
                    updated = self.edit_project(pid, new_name, new_desc)
                    print(f"✏️ Project '{updated.name}' updated successfully.")

                elif command == "delete":
                    pid = int(input("Project ID: "))
                    self.delete_project(pid)
                    print(f"🗑️ Project {pid} deleted.")

                elif command == "add":
                    pid = int(input("Project ID: "))
                    title = input("Task title: ").strip()
                    desc = input("Description (optional): ").strip()
                    task = self.add_task(pid, title, desc)
                    print(f"🆕 Task '{task.title}' (ID={task.id}) added to project {pid}")

                elif command == "edit-task":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    title = input("New title: ").strip()
                    desc = input("New description: ").strip()
                    status = input("New status (todo/doing/done): ").strip().lower()
                    updated = self.edit_task(pid, tid, title, desc, status)
                    print(f"✏️ Task '{updated.title}' updated successfully.")

                elif command == "delete-task":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    self.delete_task(pid, tid)
                    print(f"🗑️ Task {tid} deleted from project {pid}.")

                elif command == "status":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    new_status = input("New status (todo/doing/done): ").strip().lower()
                    updated = self.change_status(pid, tid, new_status)
                    print(f"🔄 Task '{updated.title}' status changed to {updated.status}.")

                elif command == "tasks":
                    pid = int(input("Project ID: "))
                    tasks = self.list_tasks(pid)
                    if not tasks:
                        print("⚠️ No tasks for this project.")
                    else:
                        print(f"\n📋 Tasks for Project {pid}:")
                        for t in tasks:
                            print(f"  [{t.id}] {t.title} — {t.status} | {t.description or 'No description'}")

                else:
                    print("⚠️ Unknown command. Try again.")

            except ValidationError as e:
                print(f"❌ {e}")
            except ValueError:
                print("❌ Invalid input type. Use numbers for IDs.")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main(argv: Optional[List[str]] = None) -> int:
    _ = argv or sys.argv[1:]
    app = ToDoApp.from_env()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
