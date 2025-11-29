ToDoList – Web API (FastAPI + PostgreSQL)

This project is a fully modular To-Do List backend.
In Phase 3, the project becomes a full Web API using FastAPI and PostgreSQL.
The old CLI (Phases 1 & 2) still exists but is deprecated.

✔ Main Features

Project management (create, list, get, delete)

Task management (create, list, get, update, delete)

Status workflow: TODO → IN_PROGRESS → DONE

Validation for names, descriptions, dates, statuses

Configurable limits via .env
Architecture Overview
todolist/
│
├── app/
│   ├── api/
│   │   ├── routes/       # FastAPI route definitions
│   │   ├── schemas.py    # Pydantic schemas
│   │   └── main.py       # FastAPI entry point
│   │
│   ├── services/         # Business logic layer
│   ├── repositories/     # Database access layer
│   ├── models/           # SQLAlchemy ORM models
│   └── db/               # Engine + session + Alembic setup
│
├── alembic/              # Migration scripts
├── docker-compose.yml    # PostgreSQL container
├── .env                  # Environment variables
├── main.py               # Legacy CLI (deprecated)
└── README.md


Architecture follows a clean layered structure:
API → Service → Repository → Model → DB
Installation & Setup
1️⃣ Install dependencies
poetry install

2️⃣ Start PostgreSQL (Docker)
docker compose up -d

3️⃣ Apply migrations
poetry run alembic upgrade head

4️⃣ Run the FastAPI server
poetry run uvicorn todolist.app.api.main:app --reload

5️⃣ Open API documentation
http://127.0.0.1:8000/docs
Environment Variables

Example .env file:

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=todolist

MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=100


These values control database connection and project/task limits.

📌 Example API Requests
Create a project
POST /api/projects/
{
  "name": "Demo",
  "description": "My project"
}

Create a task
POST /api/projects/1/tasks/
{
  "title": "Implement backend",
  "status": "TODO",
  "deadline": "2025-12-20T10:00:00"
}
Update a task (partial update)
PATCH /api/projects/1/tasks/3
{
  "status": "DONE"
}

Delete a task
DELETE /api/projects/1/tasks/5

🕹 Legacy CLI (Deprecated)

The original CLI from earlier phases still works:

poetry run python main.py


But on startup you will see:

WARNING: CLI interface is deprecated. Please use the FastAPI Web API instead.


The CLI is no longer maintained.
README – Section 6/6
🧰 Technologies Used

Python 3.12

FastAPI

SQLAlchemy ORM

Alembic

PostgreSQL

Docker

Poetry

Fully typed code (PEP 484)

📈 Optional Future Improvements

JWT authentication

Pagination

Async SQLAlchemy

CI/CD pipeline

React/Vue frontend

Unit tests (pytest)

🎯 Final Notes

This README documents the final integrated version of the ToDoList project, fully implementing the Web API from Phase 3 while preserving the earlier CLI in deprecated form.

The project now follows a clean layered structure and provides a complete, Dockerized, database-backed backend service with automatic OpenAPI documentation.