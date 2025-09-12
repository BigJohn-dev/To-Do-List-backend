
from datetime import datetime
from src.repositories import task_repository, tag_repository
from src.models.task import Task

def create_task(data):
    title = data.get("title")
    if not title:
        return {"error": "Title is required"}, 400

    due_date = None
    if "due_date" in data and data["due_date"]:
        try:
            due_date = datetime.fromisoformat(data["due_date"])
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"}, 400

    new_task = Task(
        title=title,
        due_date=due_date,
        time_estimate=data.get("time_estimate")
    )

    if "tags" in data:
        for tag_name in data["tags"]:
            tag = tag_repository.get_or_create_tag(tag_name)
            new_task.tags.append(tag)

    return task_repository.save_task(new_task).to_dict()


def update_task(task_id, data):
    task = task_repository.get_task(task_id)
    if not task:
        return None

    if "title" in data:
        task.title = data["title"]

    if "completed" in data:
        task.completed = data["completed"]

    if "due_date" in data and data["due_date"]:
        task.due_date = datetime.fromisoformat(data["due_date"])

    if "time_estimate" in data:
        task.time_estimate = data["time_estimate"]

    if "tags" in data:
        task.tags.clear()
        for tag_name in data["tags"]:
            tag = tag_repository.get_or_create_tag(tag_name)
            task.tags.append(tag)

    return task_repository.update_task(task).to_dict()


def list_tasks():
    return [task.to_dict() for task in task_repository.get_all_tasks()]


def remove_task(task_id):
    task = task_repository.get_task(task_id)
    if task:
        task_repository.delete_task(task)
        return True
    return False
