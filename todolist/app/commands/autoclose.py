from datetime import datetime, timezone
from todolist.app.persistence.db import SessionLocal
from todolist.app.persistence.repositories.task_repository import TaskRepository
from todolist.app.persistence.models.task import status_enum  # Using status_enum for reference


def autoclose_overdue_tasks() -> None:
    """Automatically close overdue tasks."""
    db = SessionLocal()
    repo = TaskRepository(db)

    now = datetime.now(timezone.utc)

    # --- FIX: Calling the new method that retrieves all tasks ---
    tasks = repo.get_all_tasks()

    closed_count = 0
    for task in tasks:
        # Check if overdue and not already done ('DONE' is the string value from the ENUM)
        if task.deadline and task.deadline < now and task.status != 'DONE':
            task.status = 'DONE'
            task.closed_at = now  # Record the completion time
            closed_count += 1

    db.commit()
    print(f"✅ {closed_count} overdue tasks automatically closed at {now.isoformat()}")

    db.close()