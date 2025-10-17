from todolist.core.services import ToDoApp


def main() -> None:
    """Application entry point."""
    app = ToDoApp.from_env()
    app.run()


if __name__ == "__main__":
    main()
