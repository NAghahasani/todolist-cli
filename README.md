# README: To-Do List Manager System

The To-Do List Manager is a scalable task management system built using Python, FastAPI, and a clear Layered Architecture (Services/Repositories). The primary focus is providing a robust REST API for data interaction.

Status | Tech Stack | Architecture | License
:---: | :---: | :---: | :---:
🟢 Ready | Python 3.11+, FastAPI, Poetry | Layered (Services/Repositories) | MIT

---

# 🚀 Getting Started

This project uses Poetry for dependency management.

### 1. Prerequisites

* Python 3.11+
* Poetry (Install using: pip install poetry)

### 2. Installation

Install all required libraries defined in pyproject.toml using Poetry:

poetry install

### 3. Database Setup (Migrations)

To initialize the database structure and apply the SQLAlchemy models, use Alembic migrations:

# Apply all pending migrations
poetry run alembic upgrade head

---

# 🏃 Running the API (Main Application)

The core API is executed using uvicorn. Use the --reload flag during development for automatic restart on code changes.

poetry run uvicorn todolist.app.api.main:app --reload

### 🌍 API Access

The API will be available at:

👉 http://127.0.0.1:8000

---

# 📖 Documentation & Testing

### 1. Interactive Documentation (Swagger UI)

FastAPI automatically generates comprehensive API documentation. You can view and test all endpoints interactively:

🔗 Swagger URL: http://127.0.0.1:8000/docs

### 2. Postman Collection

For end-to-end testing, the repository includes a complete Postman collection:

* Collection File: _POSTMAN_COLLECTION.json
* Environment File: _POSTMAN_ENVIRONMENT.json

How to Use: Import both JSON files into Postman and ensure the "Local Development" environment is selected before running requests.

---

# ⚙️ Features and Commands

### Primary API Endpoints

Resource | Operations | HTTP Method | Description
:---: | :---: | :---: | :---:
/projects | CRUD | POST, GET, PATCH, DELETE | Manage projects. Deleting a project cascades to delete all associated tasks.
/tasks | CRUD | POST, GET, PATCH, DELETE | Manage tasks. Supports listing by project ID and updating status.

### Background Commands

A background command is included to automatically check for overdue tasks and mark them as DONE. Run it manually via the CLI:

poetry run python -m todolist.app.commands.autoclose

#### ⏰ Automation Setup (Required for Scheduled Execution)

To ensure the auto-close logic runs periodically (e.g., every 15 minutes) as required by the project, the scheduler process must be run **in a separate terminal tab**:

1.  **Run the Scheduler:** This process will continuously check the defined schedule.
    
    poetry run python todolist/app/commands/scheduler.py

2.  **Keep it running:** Do not close this terminal tab.
### ⚠️ Deprecation Notice (Important)

Attention: The legacy CLI interface is deprecated as of Phase 3. Please use the REST API for all interactions and the addition of new features.

---

# 📂 Project Structure (Architecture)

This project utilizes a layered architecture for clear separation of concerns, particularly isolating the data persistence layer.

todolist-cli/
├── alembic/                # Database migration scripts
├── todolist/
│   └── app/
│       ├── api/            # Routes, Controllers, & Pydantic Schemas
│       ├── commands/       # Background commands
│       ├── exceptions/     # Custom Exception classes
│       ├── persistence/    # Data Access Layer
│       │   ├── db/         # Database Session setup
│       │   ├── models/     # SQLAlchemy Models (Table structure)
│       │   └── repositories/ # Repository implementations (CRUD)
│       └── services/       # Core Business Logic
│
└── cli/                    # Deprecated legacy CLI interface

Layer Responsibilities:
* Services: Contains all business logic, validation, and orchestration of repositories.
* Repositories: Directly handles data access operations (CRUD) with SQLAlchemy.
* API: Handles HTTP requests, input validation (Pydantic), and delegates tasks to the Services layer.