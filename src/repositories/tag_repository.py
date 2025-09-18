from src.extensions import mongo
from bson import ObjectId

def get_or_create_tag(name):
    tag = mongo.db.tags.find_one({"name": name})
    if tag:
        return {"_id": str(tag["_id"]), "name": tag["name"]}

    result = mongo.db.tags.insert_one({"name": name})
    return {"_id": str(result.inserted_id), "name": name}


def get_tag_by_id(tag_id):
    tag = mongo.db.tags.find_one({"_id": ObjectId(tag_id)})
    if tag:
        tag["_id"] = str(tag["_id"])
    return tag


def list_tags():
    tags = list(mongo.db.tags.find())
    for tag in tags:
        tag["_id"] = str(tag["_id"])
    return tags
