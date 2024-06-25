from flask import Blueprint, render_template, redirect, request, url_for, flash

from .models import Task
from .forms import TaskForm
from .services import TasksServices

from flask_jwt_extended import get_current_user, jwt_required

web_bp = Blueprint("web", __name__)

tasks_service = TasksServices()


@web_bp.route("/")
@jwt_required()
def list_tasks():
    current_user = get_current_user()
    tasks = tasks_service.get_all_tasks()
    return render_template("/tasks/list.html", tasks=tasks, current_user=current_user)


@web_bp.route("/tasks/create", methods=["GET", "POST"])
@jwt_required()
def create_task():
    current_user = get_current_user()
    form = TaskForm()

    if request.method == "POST" and form.validate_on_submit():
        cleaned_data = {
            "title": form.title.data,
            "description": form.description.data,
            "status": form.status.data,
        }
        task = Task(**cleaned_data)
        tasks_service.create_task(task)
        return redirect(url_for("web.list_tasks"))
        
    return render_template("/tasks/create.html", form=form, current_user=current_user)


@web_bp.route("/tasks/<int:id>")
@jwt_required()
def delete_task(id):
    tasks_service.delete_task(id)
    return redirect(url_for("web.list_tasks"))
