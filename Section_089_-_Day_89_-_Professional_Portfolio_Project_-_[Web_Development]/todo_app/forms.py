from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Optional

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=[('todo', 'To Do'), ('doing', 'In Progress'), ('done', 'Done')], default='todo')
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[Optional()])
