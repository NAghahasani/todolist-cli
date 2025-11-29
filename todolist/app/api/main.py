from __future__ import annotations

from fastapi import FastAPI

from todolist.app.api.routes import projects, tasks


def create_app() -> FastAPI:
    app = FastAPI(
        title="ToDoList API",
        version="0.1.0",
    )

    app.include_router(projects.router)
    app.include_router(tasks.router)

    return app


app = create_app()
