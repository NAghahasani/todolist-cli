"""CLI ToDoList – Feature: Change Task Status (Complete)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional
from dotenv import load_dotenv
import os
import sys


Status = Literal["todo", "doing", "done"]


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

    def _find_project(self, name: str) -> Optional[Project]:
        return next((p for p in self._projects if p.name.lower() == name.lower()), None)

    def delete_project(self, name: str) -> None:
        project = self._find_project(name)
        if not project:
            raise ValidationError(f"Project '{name}' not found.")
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
        project = self._find_project(project_name)
        if not project:
            raise ValidationError(f"Project '{project_name}' not found.")
        task = next((t for t in project.tasks if t.title.lower() == task_title.strip().lower()), None)
        if not task:
            raise ValidationError(f"Task '{task_title}' not found in project '{project_name}'.")
        project.tasks.remove(task)

    def change_task_status(self, project_name: str, task_title: str, new_status: Status) -> Task:
        """Change the status of a specific task."""
        project = self._find_project(project_name)
        if not project:
            raise ValidationError(f"Project '{project_name}' not found.")
        task = next((t for t in project.tasks if t.title.lower() == task_title.strip().lower()), None)
        if not task:
            raise ValidationError(f"Task '{task_title}' not found in project '{project_name}'.")
        if new_status not in ("todo", "doing", "done"):
            raise ValidationError("Invalid status. Must be 'todo', 'doing', or 'done'.")
        task.status = new_status
        return task

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
        print("📝 ToDoList CLI — Commands: new, add, delete-task, change-status, list, exit.")

        while True:
            command = input("\n> ").strip().lower()

            if command in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            try:
                if command == "new":
                    name = input("Project name: ").strip()
                    desc = input("Description (optional): ").strip()
                    self.create_project(name, desc)
                    print(f"✅ Project '{name}' created successfully!")

                elif command == "add":
                    proj = input("Project name: ").strip()
                    title = input("Task title: ").strip()
                    desc = input("Description (optional): ").strip()
                    self.add_task(proj, title, desc)
                    print(f"🆕 Task '{title}' added to project '{proj}'")

                elif command == "delete-task":
                    proj = input("Project name: ").strip()
                    title = input("Task title to delete: ").strip()
                    self.delete_task(proj, title)
                    print(f"🗑️ Task '{title}' deleted from project '{proj}'")

                elif command == "change-status":
                    proj = input("Project name: ").strip()
                    title = input("Task title: ").strip()
                    new_status = input("New status (todo/doing/done): ").strip().lower()
                    updated = self.change_task_status(proj, title, new_status)
                    print(f"🔄 Task '{updated.title}' status updated to [{updated.status}]")

                elif command == "list":
                    projects = self.list_projects()
                    if not projects:
                        print("📂 No projects found.")
                        continue
                    print("\n📋 Projects:")
                    for i, p in enumerate(projects, start=1):
                        print(f"{i}. {p.name} ({len(p.tasks)} tasks)")
                        for j, t in enumerate(p.tasks, start=1):
                            print(f"   {j}) {t.title} — {t.status}")

                else:
                    print("⚠️ Unknown command.")

            except ValidationError as e:
                print(f"❌ {e}")


def main(argv: Optional[List[str]] = None) -> int:
    _ = argv or sys.argv[1:]
    app = ToDoApp.from_env()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
