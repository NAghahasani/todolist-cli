from __future__ import annotations
from datetime import datetime
from typing import Optional
from todolist.app.persistence.models import Status
from todolist.app.exceptions.errors import ValidationError
from todolist.app.services.project_service import ProjectService
from todolist.app.services.task_service import TaskService


class ToDoApp:
    """Core application logic for managing projects and commands (Phase 2: Database-backed).

    This class now delegates all validation and persistence logic to the Service Layer,
    adhering to Separation of Concerns.
    """

    def __init__(
            self,
            max_projects: int,
            max_tasks: int,
            project_service: Optional[ProjectService] = None,
            task_service: Optional[TaskService] = None,
    ) -> None:
        self._max_projects = max_projects
        self._max_tasks = max_tasks
        # Dependencies are injected (Constructor Injection)
        self.project_service = project_service
        self.task_service = task_service

    # ---------------- Project Operations ----------------
    def create_project(self, name: str, description: str = ""):
        # Validation (name length, blank, uniqueness) is now handled by ProjectService.
        project = self.project_service.create(
            name=name.strip(),
            description=description.strip()
        )
        print(f"✅ Project '{project.name}' created (ID={project.id})")
        return project

    def edit_project(self, pid: int, new_name: str, new_description: str):
        # Delegate update logic and uniqueness checks to the service layer.
        project = self.project_service.update(
            project_id=pid,
            new_name=new_name.strip(),
            new_description=new_description.strip()
        )
        return project

    def delete_project(self, pid: int) -> None:
        deleted = self.project_service.delete(pid)
        if not deleted:
            raise ValidationError("Project not found.")

    def list_projects(self):
        return self.project_service.get_all()

    # ---------------- Task Operations ----------------
    def add_task(
            self,
            project_id: int,
            title: str,
            description: str = "",
            deadline: Optional[str] = None,
    ):
        # Validation (title length, blank, description length, deadline format)
        # is now handled by TaskService.
        task = self.task_service.create(
            project_id=project_id,
            title=title.strip(),
            description=description.strip(),
            deadline=deadline
        )
        print(f"🆕 Task '{task.title}' added (ID={task.id})")
        return task

    def edit_task(
            self,
            project_id: int,
            task_id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[Status] = None,
            deadline: Optional[str] = None,
    ):
        # Delegate all update and validation logic to the service layer.
        updated_task = self.task_service.update(
            project_id=project_id,
            task_id=task_id,
            title=title.strip() if title else None,
            description=description.strip() if description else None,
            status=status,
            deadline=deadline
        )
        return updated_task

    def delete_task(self, project_id: int, task_id: int):
        deleted = self.task_service.delete(task_id)
        if not deleted:
            raise ValidationError("Task not found.")

    def list_tasks(self, project_id: int):
        return self.task_service.get_by_project(project_id)

    def move_task(self, project_id: int, task_id: int, new_status: Status):
        if new_status not in ("todo", "doing", "done"):
            raise ValidationError("Invalid status. Use 'todo', 'doing', or 'done'.")

        updated = self.task_service.update_task_status(task_id, new_status)
        if not updated:
            raise ValidationError("Task not found.")
        return updated

    # ---------------- CLI ----------------
    def run(self) -> None:
        # Added warning as per project documentation standard.
        print("\n" + "=" * 70)
        print("⚠️ WARNING: CLI interface is deprecated as of Phase 3.")
        print("Please use the REST API for all interactions and new features.")
        print("=" * 70 + "\n")

        print("🧱 ToDo List CLI (Phase 2: Database Mode) — type 'help' to see commands.")
        while True:
            try:
                cmd = input("\n> ").strip().lower()
                if cmd in ("exit", "quit"):
                    print("👋 Bye!")
                    break
                elif cmd == "help":
                    print(
                        "Commands:\n"
                        "  projects                - list all projects\n"
                        "  new                     - create a project\n"
                        "  editp                   - edit a project\n"
                        "  deletep                 - delete a project\n"
                        "  tasks                   - list tasks for a project\n"
                        "  add                     - add a task\n"
                        "  editt                   - edit a task\n"
                        "  deletet                 - delete a task\n"
                        "  move                    - move task status\n"
                        "  quit/exit               - exit"
                    )
                elif cmd == "projects":
                    projects = self.list_projects()
                    if not projects:
                        print("⚠️ No projects found.")
                    else:
                        print("\n📦 Projects:")
                        for p in projects:
                            print(f"  [{p.id}] {p.name} — {p.description}")
                elif cmd == "new":
                    name = input("Project name: ")
                    desc = input("Description (optional): ")
                    self.create_project(name, desc)
                elif cmd == "editp":
                    pid = int(input("Project ID: "))
                    new_name = input("New name (leave empty to keep): ")
                    new_desc = input("New description: ")
                    self.edit_project(pid, new_name, new_desc)
                    print("✏️ Project updated.")
                elif cmd == "deletep":
                    pid = int(input("Project ID: "))
                    self.delete_project(pid)
                    print("🗑️ Project deleted.")
                elif cmd == "add":
                    pid = int(input("Project ID: "))
                    title = input("Task title: ")
                    desc = input("Description (optional): ")
                    ddl = input("Deadline (YYYY-MM-DD) (optional): ").strip() or None
                    self.add_task(pid, title, desc, ddl)
                elif cmd == "editt":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    title = input("New title: ").strip() or None
                    desc = input("New description: ").strip() or None
                    st = input("New status (todo/doing/done): ").strip() or None
                    ddl = input("New deadline (YYYY-MM-DD, empty to keep): ").strip() or None
                    self.edit_task(pid, tid, title, desc, st, ddl)
                    print("✏️ Task updated.")
                elif cmd == "deletet":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    self.delete_task(pid, tid)
                    print("🗑️ Task deleted.")
                elif cmd == "move":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    st = input("New status (todo/doing/done): ").strip()
                    self.move_task(pid, tid, st)
                    print("➡️ Task moved.")
                elif cmd == "tasks":
                    pid = int(input("Project ID: "))
                    tasks = self.list_tasks(pid)
                    if not tasks:
                        print("⚠️ No tasks found.")
                    else:
                        print(f"\n📋 Tasks for Project {pid}:")
                        for t in tasks:
                            print(f"  [{t.id}] {t.title} — {t.status} | {t.description}")
                else:
                    print("⚠️ Unknown command. Try again.")
            except ValidationError as e:
                print(f"❌ {e}")
            except ValueError:
                print("❌ Invalid input. Use numeric IDs.")