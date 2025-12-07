# ToDoList Web API 🚀

A comprehensive, modular, and layered **RESTful API** for managing projects and tasks. This project demonstrates modern Python backend development practices, transitioning from a legacy CLI to a robust Web API using **FastAPI** and **PostgreSQL**.

---

## 🏗️ Architecture & Design

The project follows a strict **Layered Architecture** to ensure separation of concerns, maintainability, and scalability:

* **API Layer (Controllers):** Handles HTTP requests, input validation (Pydantic), and response formatting. (`app/api/routes`)
* **Service Layer (Business Logic):** Implements core business rules (e.g., uniqueness checks, task limits) and orchestrates data flow. (`app/services`)
* **Repository Layer (Persistence):** Manages direct database interactions using SQLAlchemy. (`app/repositories`)
* **Domain Layer (Models):** Defines database schemas and entities. (`app/models`)

---

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **Framework:** FastAPI
* **Database:** PostgreSQL 15
* **ORM:** SQLAlchemy (Sync)
* **Migration Tool:** Alembic
* **Dependency Manager:** Poetry
* **Containerization:** Docker & Docker Compose
* **Testing:** Postman Collection

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites
* Docker & Docker Compose
* Python 3.12+
* Poetry (`pip install poetry`)

### 1. Clone & Install Dependencies
```bash
git clone <your-repo-url>
cd todolist-cli
poetry install
2. Setup Environment Variables
Create a .env file in the root directory based on .env.example:

Bash

cp .env.example .env
Ensure DB_HOST=localhost, DB_PORT=5432, DB_USER=NA, DB_PASSWORD=1818 (or match your docker-compose credentials).

3. Start Database (Docker)
Launch the PostgreSQL container:

Bash

docker compose up -d
4. Apply Database Migrations
Create the tables in the database using Alembic:

Bash

poetry run alembic upgrade head
5. Run the Server
Start the FastAPI server with auto-reload:

Bash

poetry run uvicorn todolist.app.api.main:app --reload
The API will be available at: http://127.0.0.1:8000

📖 Documentation & Testing
1. Swagger UI (Auto-generated Docs)
Once the server is running, visit: 👉 http://127.0.0.1:8000/docs

You can view all endpoints and test them interactively.

2. Postman Collection (Phase 4)
This repository includes a full Postman collection for end-to-end testing.

Collection File: _POSTMAN_COLLECTION.json

Environment File: _POSTMAN_ENVIRONMENT.json

How to use:

Open Postman.

Click Import and select both JSON files from the project root.

Select the "Local Development" environment in Postman.

Run the requests!

⚙️ Features & Commands
✅ API Endpoints
Projects: Create, List, Update (Patch), Delete (Cascade).

Tasks: Create, List (by Project), Update Status, Delete.

🕒 Auto-close Overdue Tasks
A background command to check for overdue tasks and mark them as DONE. Run it manually via CLI:

Bash

poetry run python -m todolist.app.commands.autoclose
⚠️ Deprecation Notice
The legacy CLI interface (main.py) is deprecated as of Phase 3. Please use the REST API for all interactions.

📂 Project Structure
todolist-cli/
├── alembic/                # Migration scripts
├── todolist/
│   └── app/
│       ├── api/            # Routes & Pydantic Schemas
│       ├── commands/       # CLI commands (autoclose)
│       ├── core/           # Config & Utils
│       ├── db/             # Database Session
│       ├── models/         # SQLAlchemy Models
│       ├── repositories/   # CRUD Operations
│       └── services/       # Business Logic
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── README.md