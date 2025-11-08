from datetime import datetime, timezone
from todolist.app.db.session import SessionLocal
from todolist.app.repositories.task_repository import TaskRepository
from todolist.app.models.models import Status



def autoclose_overdue_tasks() -> None:
    """Automatically close overdue tasks."""
    db = SessionLocal()
    repo = TaskRepository(db)

    now = datetime.now(timezone.utc)
    tasks = repo.get_all()

    closed_count = 0
    for task in tasks:
        if task.deadline and task.deadline < now and task.status != Status.DONE:
            task.status = Status.DONE
            closed_count += 1

    db.commit()
    print(f"✅ {closed_count} overdue tasks automatically closed at {now.isoformat()}")

    db.close()
