from __future__ import annotations

from datetime import datetime
from typing import List, Optional
import os
import sys

from dotenv import load_dotenv

from todolist.data.models import Project, Task, Status
from todolist.core.validation import ValidationError


class ToDoApp:
    """Core application logic for managing projects and tasks in memory."""

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        self._projects: List[Project] = []
        self._max_projects = max_projects
        self._max_tasks = max_tasks
        self._next_pid = 1
        self._next_tid = 1

    # ---------------- Project Operations ----------------
    def create_project(self, name: str, description: str = "") -> Project:
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")

        if ValidationError.is_blank(name):
            raise ValidationError("Project name is required.")

        if not (ValidationError.NAME_MIN_LEN <= len(name) <= ValidationError.NAME_MAX_LEN):
            raise ValidationError("Invalid project name length.")

        for project in self._projects:
            if project.name.strip().lower() == name.strip().lower():
                raise ValidationError("Project name must be unique.")

        project = Project(
            id=self._next_pid,
            name=name.strip(),
            description=description.strip(),
        )
        self._projects.append(project)
        self._next_pid += 1
        return project

    def edit_project(self, pid: int, new_name: str, new_description: str) -> Project:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")

        if new_name and any(p.name.lower() == new_name.lower() and p.id != pid for p in self._projects):
            raise ValidationError("Project name already exists.")

        if new_name:
            project.name = new_name.strip()

        project.description = new_description.strip()
        return project

    def delete_project(self, pid: int) -> None:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")
        self._projects.remove(project)

    def list_projects(self) -> List[Project]:
        return sorted(self._projects, key=lambda p: p.id)

    # ---------------- Task Operations ----------------
    def add_task(
        self,
        pid: int,
        title: str,
        description: str = "",
        deadline: Optional[str] = None,
    ) -> Task:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")
        if len(project.tasks) >= self._max_tasks:
            raise ValidationError("Task limit reached.")
        if not title.strip():
            raise ValidationError("Task title required.")
        if deadline:
            self._validate_date(deadline)
        task = Task(
            id=self._next_tid,
            title=title.strip(),
            description=description.strip(),
            deadline=deadline,
        )
        project.tasks.append(task)
        self._next_tid += 1
        return task

    def edit_task(
        self,
        pid: int,
        tid: int,
        new_title: str,
        new_description: str,
        new_deadline: Optional[str],
    ) -> Task:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")
        task = self._find_task(project, tid)
        if not task:
            raise ValidationError("Task not found.")
        if new_deadline:
            self._validate_date(new_deadline)
        task.title = new_title.strip() or task.title
        task.description = new_description.strip() or task.description
        task.deadline = new_deadline or task.deadline
        return task

    def delete_task(self, pid: int, tid: int) -> None:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")
        task = self._find_task(project, tid)
        if not task:
            raise ValidationError("Task not found.")
        project.tasks.remove(task)

    def change_status(self, pid: int, tid: int, new_status: Status) -> Task:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")
        task = self._find_task(project, tid)
        if not task:
            raise ValidationError("Task not found.")
        if new_status not in ["todo", "doing", "done"]:
            raise ValidationError("Invalid status.")
        task.status = new_status
        return task

    def list_tasks(self, pid: int) -> List[Task]:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")
        return sorted(project.tasks, key=lambda t: t.id)

    # ---------------- Helpers ----------------
    def _find_project(self, pid: int) -> Optional[Project]:
        return next((p for p in self._projects if p.id == pid), None)

    def _find_task(self, project: Project, tid: int) -> Optional[Task]:
        return next((t for t in project.tasks if t.id == tid), None)

    @staticmethod
    def _validate_date(date_str: str) -> None:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Deadline must be in YYYY-MM-DD format.")

    # ---------------- Env Factory ----------------
    @staticmethod
    def from_env() -> ToDoApp:
        load_dotenv()
        try:
            max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
            max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
        except ValueError as exc:
            raise ValidationError("Environment values must be integers.") from exc
        return ToDoApp(max_projects, max_tasks)

    # ---------------- CLI ----------------
    def run(self) -> None:
        print("\n🧱 ToDoList CLI — Commands: new, editp, deletep, list, add, editt, deletet, status, tasks, exit")

        while True:
            cmd = input("\n> ").strip().lower()
            try:
                if cmd in {"exit", "quit"}:
                    print("👋 Goodbye!")
                    break
                elif cmd == "new":
                    name = input("Project name: ")
                    desc = input("Description (optional): ")
                    p = self.create_project(name, desc)
                    print(f"✅ Project '{p.name}' created (ID={p.id})")
                elif cmd == "editp":
                    pid = int(input("Project ID: "))
                    new_name = input("New name (leave empty to keep): ")
                    new_desc = input("New description: ")
                    p = self.edit_project(pid, new_name, new_desc)
                    print(f"✏️ Project '{p.name}' updated.")
                elif cmd == "deletep":
                    pid = int(input("Project ID: "))
                    self.delete_project(pid)
                    print("🗑️ Project deleted.")
                elif cmd == "list":
                    projects = self.list_projects()
                    if not projects:
                        print("⚠️ No projects found.")
                    else:
                        print("\n📋 Projects:")
                        for p in projects:
                            print(f"  [{p.id}] {p.name} — {p.description} ({len(p.tasks)} tasks)")
                elif cmd == "add":
                    pid = int(input("Project ID: "))
                    title = input("Task title: ")
                    desc = input("Description (optional): ")
                    deadline = input("Deadline (YYYY-MM-DD, optional): ").strip()
                    deadline = deadline or None
                    t = self.add_task(pid, title, desc, deadline)
                    print(f"🆕 Task '{t.title}' (ID={t.id}) added to project {pid}")
                elif cmd == "editt":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    new_title = input("New title (leave empty to keep): ")
                    new_desc = input("New description: ")
                    new_deadline = input("New deadline (YYYY-MM-DD, optional): ").strip() or None
                    t = self.edit_task(pid, tid, new_title, new_desc, new_deadline)
                    print(f"✏️ Task '{t.title}' updated.")
                elif cmd == "deletet":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    self.delete_task(pid, tid)
                    print("🗑️ Task deleted.")
                elif cmd == "status":
                    pid = int(input("Project ID: "))
                    tid = inسسt(input("Task ID: "))
                    new_status = input("New status (todo/doing/done): ").strip().lower()
                    t = self.change_status(pid, tid, new_status)
                    print(f"🔄 Task '{t.title}' updated to '{t.status}'.")
                elif cmd == "tasks":
                    pid = int(input("Project ID: "))
                    tasks = self.list_tasks(pid)
                    if not tasks:
                        print("⚠️ No tasks found for this project.")
                    else:
                        print(f"\n📋 Tasks for Project {pid}:")
                        for t in tasks:
                            print(f"  [{t.id}] {t.title} — {t.status} | {t.description} | Deadline: {t.deadline or '-'}")
                else:
                    print("⚠️ Unknown command. Try again.")
            except ValidationError as e:
                print(f"❌ {e}")
            except ValueError:
                print("❌ Invalid input. Use numeric IDs.")
