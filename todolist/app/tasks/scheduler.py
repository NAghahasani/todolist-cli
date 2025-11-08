import schedule
import time
from todolist.app.tasks.autoclose import autoclose_overdue_tasks


schedule.every(15).minutes.do(autoclose_overdue_tasks)

print("Scheduler started: running autoclose_overdue_tasks every 15 minutes...")

while True:
    schedule.run_pending()
    time.sleep(1)
