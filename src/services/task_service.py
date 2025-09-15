from datetime import datetime
from src.repositories import task_repository, tag_repository
from src.models.task import Task

def create_task(data, user_id):
    title = data.get("title")
    if not title or not title.strip():
        return {"error": "Title is required"}, 400

    existing = task_repository.get_tasks_by_user(user_id)
    if any(t.title.strip().lower() == title.strip().lower() for t in existing):
        return {"error": f"Task with title '{title}' already exists for this user"}, 400

    due_date = None
    if "due_date" in data and data["due_date"]:
        try:
            due_date = datetime.fromisoformat(data["due_date"])
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"}, 400

    time_estimate = data.get("time_estimate")
    if time_estimate is not None:
        if not isinstance(time_estimate, int) or time_estimate <= 0:
            return {"error": "time_estimate must be a positive integer"}, 400

    tags = data.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            return {"error": "tags must be a list of strings"}, 400

    new_task = Task(
        title=title.strip(),
        due_date=due_date,
        time_estimate=time_estimate,
        user_id=user_id
    )

    return task_repository.save_task(new_task).to_dict()

def update_task(task_id, data, user_id):
    task = task_repository.get_task(task_id)
    if not task or task.user_id != user_id:
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

def list_tasks(user_id):
    return [task.to_dict() for task in task_repository.get_tasks_by_user(user_id)]

def remove_task(task_id, user_id):
    task = task_repository.get_task(task_id)
    if not task or task.user_id != user_id:
        return False
    task_repository.delete_task(task)
    return True
