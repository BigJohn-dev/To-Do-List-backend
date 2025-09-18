from datetime import datetime
from bson import ObjectId
from src.extensions import mongo

class Task:
    collection = mongo.db.tasks

    def __init__(self, title, user_id, due_date=None, time_estimate=None, completed=False, tags=None):
        self.title = title
        self.user_id = ObjectId(user_id)  # store as ObjectId
        self.due_date = due_date
        self.time_estimate = time_estimate
        self.completed = completed
        self.tags = tags or []

    def save(self):
        task_data = {
            "title": self.title,
            "completed": self.completed,
            "due_date": self.due_date,
            "time_estimate": self.time_estimate,
            "user_id": self.user_id,
            "tags": self.tags,
            "created_at": datetime.utcnow()
        }
        result = Task.collection.insert_one(task_data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_user(user_id):
        return list(Task.collection.find({"user_id": ObjectId(user_id)}))

    @staticmethod
    def find_by_id(task_id):
        return Task.collection.find_one({"_id": ObjectId(task_id)})

    @staticmethod
    def update(task_id, updates):
        Task.collection.update_one({"_id": ObjectId(task_id)}, {"$set": updates})
        return Task.find_by_id(task_id)

    @staticmethod
    def delete(task_id):
        result = Task.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "time_estimate": self.time_estimate,
            "user_id": str(self.user_id),
            "tags": self.tags
        }
