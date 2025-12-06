"""
Command-line interface (CLI) for the ToDoList application.

Deprecated:
    The primary interface of the project is now the FastAPI Web API.
    This CLI is kept only for backward compatibility and educational purposes.
"""
from todolist.app.db.session import SessionLocal
from todolist.app.services.project_service import ProjectService
from todolist.app.commands.autoclose import autoclose_overdue_tasks
import sys


def main():
    """Entry point for the deprecated CLI interface."""
    print(
        "WARNING: This CLI interface is deprecated. "
        "Please use the FastAPI Web API instead."
    )
    db = SessionLocal()
    service = ProjectService(db)

    if len(sys.argv) < 2:
        print("Usage: python main.py [command] [arguments]")
        print("Commands: create_project <name> [description], list_projects, delete_project <id>, autoclose_tasks")
        return

    command = sys.argv[1]

    if command == "create_project":
        if len(sys.argv) < 3:
            print("Project name required.")
            return
        name = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        service.create_project(name, description)
        print(f"✅ Project '{name}' created successfully.")

    elif command == "list_projects":
        projects = service.list_projects()
        if not projects:
            print("No projects found.")
        else:
            print("📋 Projects:")
            for p in projects:
                print(f"- ({p.id}) {p.name}: {p.description}")

    elif command == "delete_project":
        if len(sys.argv) < 3:
            print("Project ID required.")
            return
        project_id = int(sys.argv[2])
        service.delete_project(project_id)
        print(f"🗑️ Project {project_id} deleted successfully.")

    elif command == "autoclose_tasks":
        print("Running scheduled task: autoclose overdue tasks...")
        autoclose_overdue_tasks()

    else:
        print("Unknown command.")


if __name__ == "__main__":
    main()