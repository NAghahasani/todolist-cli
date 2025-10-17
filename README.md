# 🧱 ToDoList CLI (Phase 1 – In-Memory, Modular, OOP)

A command-line ToDo list application built with Python, focusing on clean **OOP architecture**, **in-memory data management**, and strict adherence to project coding conventions.

---

## 📦 Features

### ✅ Core Functionalities
- **Project Management**
  - Create, edit, delete, and list projects.
  - Each project has a unique name and an auto-incremented ID.
- **Task Management**
  - Add, edit, delete, and list tasks for each project.
  - Task IDs are **local per project** (start from 1 for each project).
  - Edit task title, description, deadline, and status.
  - Change task status separately.
- **Cascade Delete**
  - Deleting a project removes all related tasks.
- **Validation**
  - Enforces naming rules, description length, and valid date formats.
  - Raises clear `ValidationError` messages on invalid input.
- **Environment Configuration**
  - Reads task/project limits from `.env`:
    ```
    MAX_NUMBER_OF_PROJECT=10
    MAX_NUMBER_OF_TASK=100
    ```

---

## 🧩 Architecture Overview

Project follows a modular structure:

todolist-cli/
│
├── todolist/
│ ├── data/
│ │ └── models.py # Data models (Project, Task)
│ │
│ ├── core/
│ │ ├── config.py # Env config loader
│ │ ├── services.py # Main business logic (ToDoApp)
│ │ └── validation.py # Validation and custom exceptions
│ │
│ └── cli/
│ └── app.py # CLI interface (future extension)
│
├── main.py # Entry point
├── .env # Environment configuration
├── .env.example # Example env file
└── README.md


---

## ⚙️ Run Instructions

### Using Poetry
```bash
poetry install
poetry run python main.py
CLI Commands
Command	Description
new	Create a new project
editp	Edit project name or description
deletep	Delete a project (cascade deletes tasks)
list	List all projects
add	Add a task to a project
editt	Edit task title, description, deadline, or status
deletet	Delete a task by ID (within the project)
status	Change task status (todo, doing, done)
tasks	List all tasks for a given project
exit	Quit the application

🧪 Example
pgsql
Copy code
> new
Project name: Demo
Description (optional): test project
✅ Project 'Demo' created (ID=1)

> add
Project ID: 1
Task title: Write report
Deadline (YYYY-MM-DD, optional): 2025-10-30
🆕 Task 'Write report' (ID=1) added to project 1

> tasks
📋 Tasks for Project 1:
  [1] Write report — todo | Deadline: 2025-10-30

> editt
Project ID: 1
Task ID: 1
New title (leave empty to keep): Final report
New status (todo/doing/done, leave empty to keep): done
✏️ Task 'Final report' updated. Current status: done

> exit
👋 Goodbye!
🧰 Development Notes
Language: Python 3.12

Dependency Manager: Poetry

Coding Standards: PEP8 + project-specific conventions

Data Persistence: None (In-Memory only – Phase 2 will add JSON/SQLite)

Error Handling: Centralized via ValidationError and AppError

🚀 Next Steps (Phase 2)
Add persistence layer (JSON / SQLite)

Implement cli/app.py with argparse or click

Write unit tests with pytest

Extend README with usage examples and developer guide
