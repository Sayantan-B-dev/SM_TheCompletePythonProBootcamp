from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

def _get_utc_now():
    """Return naive UTC datetime (for SQLite compatibility)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=_get_utc_now)
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')          # todo, doing, done
    priority = db.Column(db.String(20), default='medium')      # low, medium, high
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=_get_utc_now)
    updated_at = db.Column(db.DateTime, default=_get_utc_now, onupdate=_get_utc_now)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'