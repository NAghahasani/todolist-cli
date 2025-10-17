"""CLI ToDoList – Feature: Edit Task (Complete)."""
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

    # --------------------- Project Management ---------------------

    def create_project(self, name: str, description: str = "") -> Project:
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")
        if ValidationError._is_blank(name):
            raise ValidationError("Project name is required.")
        for p in self._projects:
            if p.name.strip().lower() == name.strip().lower():
                raise ValidationError("Project name must be unique.")
        project = Project(name=name.strip(), description=description.strip())
        self._projects.append(project)
        return project

    def _find_project(self, name: str) -> Optional[Project]:
        return next((p for p in self._projects if p.name.lower() == name.lower()), None)

    def list_projects(self) -> List[Project]:
        return self._projects

    # --------------------- Task Management ---------------------

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

    def edit_task(
        self,
        project_name: str,
        old_title: str,
        new_title: str,
        new_description: str = "",
        new_status: Optional[Status] = None,
    ) -> Task:
        project = self._find_project(project_name)
        if not project:
            raise ValidationError(f"Project '{project_name}' not found.")
        task = next((t for t in project.tasks if t.title.lower() == old_title.lower()), None)
        if not task:
            raise ValidationError(f"Task '{old_title}' not found in project '{project_name}'.")
        if ValidationError._is_blank(new_title):
            raise ValidationError("New task title cannot be empty.")
        task.title = new_title.strip()
        task.description = new_description.strip()
        if new_status:
            if new_status not in ("todo", "doing", "done"):
                raise ValidationError("Invalid status value.")
            task.status = new_status
        return task

    # --------------------- Environment Factory ---------------------

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
        print("📝 ToDoList CLI — Commands: new, add, edit-task, list, exit.")

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

                elif command == "edit-task":
                    proj = input("Project name: ").strip()
                    old_title = input("Current task title: ").strip()
                    new_title = input("New task title: ").strip()
                    new_desc = input("New description (optional): ").strip()
                    new_status = input("New status (todo/doing/done, optional): ").strip().lower() or None
                    updated = self.edit_task(proj, old_title, new_title, new_desc, new_status)
                    print(f"✏️ Task updated successfully → '{updated.title}' [{updated.status}]")

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
