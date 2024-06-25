from marshmallow import fields, validate, post_load

from ..extensions import ma
from .models import User
from .constants import (
    USERNAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
)


class UserResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserRegisterSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = fields.String(
        validate=validate.And(
            validate.Length(min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH),
            validate.Regexp(r"^(?!\d)[a-zA-Z0-9_]+$"),
        ),
        required=True,
    )

    email = fields.Email(
        validate=validate.Length(max=EMAIL_MAX_LENGTH),
        required=True,
    )
    password = fields.String(
        validate=validate.Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH),
        required=True,
    )

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class UserLoginSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("email", "password")
