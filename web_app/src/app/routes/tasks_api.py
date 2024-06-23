from flask import Blueprint, jsonify, request

from ..models.task import Task
from ..schemas.tasks import TaskResponseSchema, TaskCreationSchema
from ..services.tasks_services import TasksServices

from ..constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

tasks_api_bp = Blueprint("tasks_api", __name__, url_prefix="/api/tasks")

tasks_service = TasksServices()


@tasks_api_bp.route("/")
def get_all_tasks():
    tasks = tasks_service.get_all_tasks()
    schema = TaskResponseSchema(many=True)
    serialized_tasks = schema.dump(tasks)
    return jsonify(serialized_tasks), HTTP_200_OK


@tasks_api_bp.post("/")
def create_task():
    data = request.json
    schema = TaskCreationSchema()
    task: Task = schema.load(data)
    tasks_service.create_task(task)
    return (
        jsonify({"message": f"Task '{task.title}' created successfuly"}),
        HTTP_201_CREATED,
    )


@tasks_api_bp.delete("/<int:id>")
def delete_task(id):
    tasks_service.delete_task(id)
    return "", HTTP_204_NO_CONTENT
