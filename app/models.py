from flask import current_app, json
from datetime import datetime
from app import db

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return obj.data()
        else:
            return json.JSONEncoder.default(self, obj)


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'

    def data(self):
        return {
            "id": self.task_id,
            "description": self.description,
            "is_complete": bool(self.completed_at),
            "title": self.title
        }
