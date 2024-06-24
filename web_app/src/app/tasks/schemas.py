from marshmallow import Schema, fields, validate, post_load

from ..extensions import ma
from .models import Task

TASK_STATUS_CHOICES = {"pending", "completed"}


class TaskResponseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status")


class TaskCreationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task

    title = ma.auto_field()
    description = ma.auto_field(required=False)
    status = fields.String(validate=validate.OneOf(TASK_STATUS_CHOICES), required=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)
