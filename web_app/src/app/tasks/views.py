from flask import Blueprint, render_template, redirect, request, url_for, flash

from .models import Task
from .forms import TaskForm
from .services import TasksServices

web_bp = Blueprint("web", __name__)

tasks_service = TasksServices()


@web_bp.route("/")
def list_tasks():
    tasks = tasks_service.get_all_tasks()
    return render_template("/tasks/list.html", tasks=tasks)


@web_bp.route("/tasks/create", methods=["GET", "POST"])
def create_task():
    form = TaskForm()

    if request.method == "POST" and form.validate_on_submit():
        cleaned_data = {
            "title": form.title.data,
            "description": form.description.data,
            "status": form.status.data,
        }
        task = Task(**cleaned_data)
        tasks_service.create_task(task)
        flash("Task created successfully!", "success")
        return redirect(url_for("web.list_tasks"))
        
    return render_template("/tasks/create.html", form=form)


@web_bp.route("/tasks/<int:id>")
def delete_task(id):
    tasks_service.delete_task(id)
    flash("Task deleted successfully!", "success")
    return redirect(url_for("web.list_tasks"))
