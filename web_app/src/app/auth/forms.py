from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    EmailField,
    PasswordField,
)
from wtforms.validators import DataRequired, Length, EqualTo

from .constants import (
    USERNAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
)


class LoginForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Length(max=EMAIL_MAX_LENGTH)]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH),
        ],
    )
    submit = SubmitField("Sign in")


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email", validators=[DataRequired(), Length(max=EMAIL_MAX_LENGTH)]
    )
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign up")
