from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=20)])
    description = TextAreaField("Description", validators=[Length(max=150)])
    status = SelectField(
        "Status",
        choices=[("pending", "Pending"), ("completed", "Completed")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Add task")
