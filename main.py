import sys, os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

todolist_root = os.path.join(project_root, "todolist")
if todolist_root not in sys.path:
    sys.path.insert(0, todolist_root)
from todolist.app.db.session import SessionLocal
from todolist.app.services.project_service import ProjectService
from todolist.app.services.task_service import TaskService
from todolist.core.services import ToDoApp
from todolist.core.config import load_config


def main() -> None:
    """Application entry point (Phase 2 with Database)."""

    # Load configuration
    cfg = load_config()

    # Initialize database session
    db = SessionLocal()

    # Initialize services (now connected to PostgreSQL)
    project_service = ProjectService(db)
    task_service = TaskService(db)

    # Pass services into the app
    app = ToDoApp(cfg.max_projects, cfg.max_tasks, project_service, task_service)
    app.run()


if __name__ == "__main__":
    main()
