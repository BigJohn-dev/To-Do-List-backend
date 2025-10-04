from datetime import datetime
from src.repositories import task_repository, tag_repository
from bson import ObjectId
from src.extensions import mongo


def create_task(data, user_id):
    title = data.get("title")
    if not title or not title.strip():
        return {"error": "Title is required"}, 400

    existing = task_repository.get_tasks_by_user(user_id)
    if any(t["title"].strip().lower() == title.strip().lower() for t in existing):
        return {"error": f"Task with title '{title}' already"}, 400

    due_date = None
    if "due_date" in data and data["due_date"]:
        try:
            due_date = datetime.fromisoformat(data["due_date"])
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"}, 400

    if due_date < datetime.now():
        return {"error": "Invalid date setting"}, 400

    time_estimate = data.get("time_estimate")
    if time_estimate is not None:
        if not isinstance(time_estimate, int) or time_estimate <= 0:
            return {"error": "time_estimate must be a positive integer"}, 400

    tags = data.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            return {"error": "tags must be a list of strings"}, 400

    new_task = {
        "title": title.strip(),
        "completed": False,
        "due_date": due_date.isoformat() if due_date else None,
        "time_estimate": time_estimate,
        "user_id": user_id,
        "tags": tags or [],
    }

    return task_repository.save_task(new_task)


def update_task(task_id, data, user_id):
    try:
        task_obj_id = ObjectId(task_id)
    except Exception:
        return {"error": "Invalid task_id"}, 400

    task = mongo.db.tasks.find_one({"_id": task_obj_id, "user_id": str(user_id)})
    if not task:
        return None

    update_data = {}

    if "title" in data:
        update_data["title"] = data["title"].strip()

    if "completed" in data:
        update_data["completed"] = bool(data["completed"])

    if "due_date" in data and data["due_date"]:
        update_data["due_date"] = data["due_date"]

    if "time_estimate" in data:
        update_data["time_estimate"] = data["time_estimate"]

    if "tags" in data and isinstance(data["tags"], list):
        update_data["tags"] = data["tags"]

    if update_data:
        mongo.db.tasks.update_one(
            {"_id": task_obj_id, "user_id": str(user_id)},
            {"$set": update_data}
        )
    updated_task = mongo.db.tasks.find_one({"_id": task_obj_id})
    updated_task["_id"] = str(updated_task["_id"])
    return updated_task


def list_tasks(user_id):
    tasks_cursor = mongo.db.tasks.find({"user_id": user_id})

    tasks = []
    for task in tasks_cursor:
        task["_id"] = str(task["_id"])
        tasks.append(task)

    return tasks


def remove_task(task_id, user_id):
    task = task_repository.get_task(task_id)
    if not task or task.get("user_id") != user_id:
        return {"error": "Task not found"}, 404
    task_repository.delete_task(task_id)
    return {"message": "Task deleted successfully"}, 200
