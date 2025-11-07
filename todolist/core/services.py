from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from todolist.data.models import Project, Task, Status
from todolist.core.validation import ValidationError


class ToDoApp:
    """Core application logic for managing projects and tasks in memory."""

    def __init__(self, max_projects: int, max_tasks: int) -> None:
        self._projects: List[Project] = []
        self._max_projects = max_projects
        self._max_tasks = max_tasks
        self._next_pid = 1

    # ---------------- Project Operations ----------------
    def create_project(self, name: str, description: str = "") -> Project:
        if len(self._projects) >= self._max_projects:
            raise ValidationError("Project limit reached.")

        if ValidationError.is_blank(name):
            raise ValidationError("Project name is required.")

        if len(name.strip()) > 30:
            raise ValidationError("Project name must be less than 30 characters.")

        if len(description.strip()) > 150:
            raise ValidationError("Project description must be less than 150 characters.")

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
            if ValidationError.is_blank(new_name):
                raise ValidationError("Project name cannot be blank.")
            if len(new_name.strip()) > 30:
                raise ValidationError("Project name must be less than 30 characters.")
            project.name = new_name.strip()

        if new_description is not None:
            if len(new_description.strip()) > 150:
                raise ValidationError("Project description must be less than 150 characters.")
            project.description = new_description.strip()

        return project

    def delete_project(self, pid: int) -> None:
        project = self._find_project(pid)
        if not project:
            raise ValidationError("Project not found.")
        self._projects.remove(project)

    def list_projects(self) -> List[Project]:
        return list(self._projects)

    # ---------------- Task Operations ----------------
    def add_task(
        self,
        project_id: int,
        title: str,
        description: str = "",
        deadline: Optional[str] = None,
    ) -> Task:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")

        if len(project.tasks) >= self._max_tasks:
            raise ValidationError("Task limit reached for this project.")

        if ValidationError.is_blank(title):
            raise ValidationError("Task title is required.")

        if len(title.strip()) > 50:
            raise ValidationError("Task title must be less than 50 characters.")

        if len(description.strip()) > 200:
            raise ValidationError("Task description must be less than 200 characters.")

        if deadline is not None:
            self._validate_deadline(deadline)

        next_tid = (max((t.id for t in project.tasks), default=0) + 1)
        task = Task(
            id=next_tid,
            title=title.strip(),
            description=description.strip(),
            status="todo",
            deadline=deadline,
        )
        project.tasks.append(task)
        return task

    def edit_task(
        self,
        project_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[Status] = None,
        deadline: Optional[str] = None,
    ) -> Task:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = self._find_task(project, task_id)
        if not task:
            raise ValidationError("Task not found.")

        if title is not None:
            if ValidationError.is_blank(title):
                raise ValidationError("Task title cannot be blank.")
            if len(title.strip()) > 50:
                raise ValidationError("Task title must be less than 50 characters.")
            task.title = title.strip()

        if description is not None:
            if len(description.strip()) > 200:
                raise ValidationError("Task description must be less than 200 characters.")
            task.description = description.strip()

        if status is not None:
            if status not in ("todo", "doing", "done"):
                raise ValidationError("Invalid status. Use 'todo', 'doing', or 'done'.")
            task.status = status

        if deadline is not None:
            self._validate_deadline(deadline)
            task.deadline = deadline

        return task

    def delete_task(self, project_id: int, task_id: int) -> None:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")
        task = self._find_task(project, task_id)
        if not task:
            raise ValidationError("Task not found.")
        project.tasks.remove(task)

    def list_tasks(self, project_id: int) -> List[Task]:
        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")
        return list(project.tasks)

    def move_task(self, project_id: int, task_id: int, new_status: Status) -> Task:
        if new_status not in ("todo", "doing", "done"):
            raise ValidationError("Invalid status. Use 'todo', 'doing', or 'done'.")

        project = self._find_project(project_id)
        if not project:
            raise ValidationError("Project not found.")

        task = self._find_task(project, task_id)
        if not task:
            raise ValidationError("Task not found.")

        task.status = new_status
        return task

    # ---------------- Helpers ----------------
    def _find_project(self, pid: int) -> Optional[Project]:
        return next((p for p in self._projects if p.id == pid), None)

    def _find_task(self, project: Project, tid: int) -> Optional[Task]:
        return next((t for t in project.tasks if t.id == tid), None)

    def _validate_deadline(self, date_str: str) -> None:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Deadline must be in YYYY-MM-DD format.")

    # ---------------- CLI ----------------
    def run(self) -> None:
        print("\n🧱 ToDo List CLI — type 'help' to see commands.")
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
                            print(f"  [{p.id}] {p.name} — {p.description} ({len(p.tasks)} tasks)")
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
                elif cmd == "add":
                    pid = int(input("Project ID: "))
                    title = input("Task title: ")
                    desc = input("Description (optional): ")
                    ddl = input("Deadline (YYYY-MM-DD) (optional): ").strip() or None
                    t = self.add_task(pid, title, desc, ddl)
                    print(f"🆕 Task '{t.title}' added (ID={t.id})")
                elif cmd == "editt":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    title = input("New title (leave empty to keep): ").strip() or None
                    desc = input("New description: ").strip() or None
                    st = input("New status (todo/doing/done): ").strip() or None
                    st_val: Optional[Status] = st if st in ("todo", "doing", "done") else None
                    ddl = input("New deadline (YYYY-MM-DD, empty to clear / keep): ").strip()
                    ddl_val = None if ddl == "" else ddl
                    t = self.edit_task(pid, tid, title, desc, st_val, ddl_val)
                    print(f"✏️ Task '{t.title}' updated.")
                elif cmd == "deletet":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    self.delete_task(pid, tid)
                    print("🗑️ Task deleted.")
                elif cmd == "move":
                    pid = int(input("Project ID: "))
                    tid = int(input("Task ID: "))
                    st = input("New status (todo/doing/done): ").strip()
                    t = self.move_task(pid, tid, st)  # type: ignore[arg-type]
                    print(f"➡️ Task '{t.title}' moved to {t.status}.")
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
