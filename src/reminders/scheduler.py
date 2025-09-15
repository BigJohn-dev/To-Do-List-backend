from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import app
from src.repositories import task_repository
import logging

reminder_cache = []

logging.basicConfig(level=logging.INFO)

def check_reminders():
    global reminder_cache
    now = datetime.utcnow()
    with app.app_context():
        upcoming_tasks = task_repository.get_all_tasks()

    due_soon = []
    for task in upcoming_tasks:
        if task.due_date and not task.completed:
            if now >= task.due_date - timedelta(minutes=60) and now < task.due_date:
                due_soon.append(task.to_dict())

    reminder_cache = due_soon
    if due_soon:
        logging.info(f"🔔 Found {len(due_soon)} task(s) due soon.")

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_reminders, trigger="interval", seconds=60)
    scheduler.start()
