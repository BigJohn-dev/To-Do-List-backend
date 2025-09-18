from src.extensions import mongo
from bson import ObjectId

def save_task(task):
    result = mongo.db.tasks.insert_one(task)
    return str(result.inserted_id)

def get_task(task_id):
    return mongo.db.tasks.find_one({"_id": ObjectId(task_id)})

def get_all_tasks():
    return list(mongo.db.tasks.find())

def get_tasks_by_user(user_id):
    return list(mongo.db.tasks.find({"user_id": ObjectId(user_id)}))

def update_task(task_id, updates):
    mongo.db.tasks.update_one({"_id": ObjectId(task_id)}, {"$set": updates})
    return get_task(task_id)

def delete_task(task_id):
    result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0
