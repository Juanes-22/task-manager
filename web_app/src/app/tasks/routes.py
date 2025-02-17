from flask import Blueprint, jsonify, request

from .models import Task
from .schemas import TaskResponseSchema, TaskCreationSchema
from .services import TasksServices

from ..constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from ..auth.decorators import auth_role
from flask_jwt_extended import jwt_required

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

tasks_service = TasksServices()


@tasks_bp.route("/")
@jwt_required()
@auth_role("admin")
def get_all_tasks():
    tasks = tasks_service.get_all_tasks()
    schema = TaskResponseSchema(many=True)
    serialized_tasks = schema.dump(tasks)
    return jsonify(serialized_tasks), HTTP_200_OK


@tasks_bp.post("/")
@jwt_required()
@auth_role("admin")
def create_task():
    data = request.json
    schema = TaskCreationSchema()
    task: Task = schema.load(data)
    tasks_service.create_task(task)
    return (
        jsonify({"message": f"Task '{task.title}' created successfuly"}),
        HTTP_201_CREATED,
    )


@tasks_bp.delete("/<int:id>")
@jwt_required()
@auth_role("admin")
def delete_task(id):
    tasks_service.delete_task(id)
    return "", HTTP_204_NO_CONTENT
