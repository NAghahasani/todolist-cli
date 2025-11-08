from todolist.app.db.session import SessionLocal
from todolist.app.services.project_service import ProjectService
import sys


def main():
    db = SessionLocal()
    service = ProjectService(db)

    if len(sys.argv) < 2:
        print("Usage: python main.py [command] [arguments]")
        print("Commands: create_project <name> [description], list_projects, delete_project <id>")
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

    else:
        print("Unknown command.")


if __name__ == "__main__":
    main()
