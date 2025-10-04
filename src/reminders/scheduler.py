from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import current_app
from src.repositories import task_repository
import logging

reminder_cache = []

logging.basicConfig(level=logging.INFO)


def check_reminders():
    global reminder_cache
    now = datetime.utcnow()

    # Use the current app context properly
    with current_app.app_context():
        upcoming_tasks = task_repository.get_all_tasks()

    due_soon = []
    for task in upcoming_tasks:
        due_date = task.get("due_date")
        completed = task.get("completed", False)

        if due_date and not completed:
            # Ensure due_date is a datetime object
            if isinstance(due_date, str):
                due_date = datetime.fromisoformat(due_date)

            if now >= due_date - timedelta(minutes=60) and now < due_date:
                due_soon.append(task)

    reminder_cache = due_soon
    if due_soon:
        logging.info(f"🔔 Found {len(due_soon)} task(s) due soon.")


def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_reminders, trigger="interval", seconds=60)
    scheduler.start()

