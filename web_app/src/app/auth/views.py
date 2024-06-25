from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)

from .forms import LoginForm, RegisterForm
from .services import AuthServices
from ..common.exceptions import BusinessError
from ..auth.models import User

auth_web_bp = Blueprint("auth_web", __name__)

auth_service = AuthServices()


@auth_web_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            try:
                user = auth_service.login(email, password)
                flash("User logged successfully!", "success")
                identity = {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                }
                access_token = create_access_token(identity=identity)
                refresh_token = create_refresh_token(identity=identity)

                response = redirect(url_for("web.list_tasks"))
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
            except BusinessError as exc:
                flash(exc.message, "danger")
        else:
            flash(f"{form.errors}", "danger")

    return render_template("auth/login.html", form=form)


@auth_web_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            cleaned_data = {
                "email": form.email.data,
                "username": form.username.data,
                "password": form.password.data,
            }
            user = User(**cleaned_data)
            try:
                auth_service.register(user)
                flash("User registered successfully!", "success")
                return redirect(url_for("web.list_tasks"))
            except BusinessError as exc:
                flash(exc.message, "danger")
        else:
            flash(f"{form.errors}", "danger")

    return render_template("auth/register.html", form=form)
