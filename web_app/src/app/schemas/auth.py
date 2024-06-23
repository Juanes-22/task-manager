from marshmallow import fields, validate, post_load

from ..extensions import ma
from ..models.auth import User


class UserResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserRegisterSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = fields.String(
        validate=validate.And(
            validate.Length(max=20), validate.Regexp(r"^(?!\d)[a-zA-Z0-9_]+$")
        ),
        required=True,
    )

    email = fields.Email(
        validate=validate.Length(max=100),
        required=True,
    )
    password = fields.String(
        validate=validate.Length(min=8, max=30)
    )

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class UserLoginSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("email", "password")
