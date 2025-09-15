from flask import Blueprint, request
from flask import jsonify
from src.controllers.auth_controller import token_required
from src.reminders.scheduler import reminder_cache
from src.services import task_service

task_bp = Blueprint("task_bp", __name__)

@task_bp.route("/", methods=["GET"])
@token_required
def get_tasks(current_user):
    return jsonify(task_service.list_tasks(current_user.id))

@task_bp.route("/add_task", methods=["POST"])
@token_required
def add_task(current_user):
    data = request.get_json()
    task = task_service.create_task(data, current_user.id)
    return jsonify(task), 201

@task_bp.route("/<int:task_id>", methods=["PUT"])
@token_required
def update_task(current_user, task_id):
    data = request.json
    updated = task_service.update_task(task_id, data, current_user.id)
    if updated:
        return jsonify(updated)
    return jsonify({"error": "Task not found or not yours"}), 404


@task_bp.route("/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user, task_id):
    deleted = task_service.remove_task(task_id, current_user.id)
    if deleted:
        return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found or not yours"}), 404


@task_bp.route("/reminders", methods=["GET"])
@token_required
def get_reminders(user_id):
    return jsonify(reminder_cache)

