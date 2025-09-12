from flask import Blueprint, request, jsonify
from src.services import task_service
from flask import jsonify
from src.reminders.scheduler import reminder_cache

task_bp = Blueprint("task_bp", __name__)

@task_bp.route("/", methods=["GET"])
def get_tasks():
    return jsonify(task_service.list_tasks())

@task_bp.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    new_task = task_service.create_task(data)
    return jsonify(new_task), 201

@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    updated = task_service.update_task(task_id, data)
    if updated:
        return jsonify(updated)
    return jsonify({"error": "Task not found"}), 404


@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = task_service.remove_task(task_id)
    if deleted:
        return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

@task_bp.route("/reminders", methods=["GET"])
def get_reminders():
    return jsonify(reminder_cache)

