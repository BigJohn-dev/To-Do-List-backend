from src.extensions import db
from src.models.task import Task

def get_all_tasks():
    return Task.query.all()

def get_task(task_id):
    return Task.query.get(task_id)

def save_task(task):
    db.session.add(task)
    db.session.commit()
    return task

def update_task(task):
    db.session.add(task)
    db.session.commit()
    return task

def delete_task(task):
    db.session.delete(task)
    db.session.commit()
