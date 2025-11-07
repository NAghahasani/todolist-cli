from todolist.core.services import ToDoApp
from todolist.core.config import load_config


def main() -> None:
    """Application entry point."""
    cfg = load_config()
    app = ToDoApp(cfg.max_projects, cfg.max_tasks)
    app.run()


if __name__ == "__main__":
    main()
