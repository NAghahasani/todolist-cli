from __future__ import annotations

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure FastAPI application instance."""
    app = FastAPI(
        title="ToDoList API",
        version="0.1.0",
    )

    # TODO: include routers here later (projects, tasks, ...)
    return app


app = create_app()
