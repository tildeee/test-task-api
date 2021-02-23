from flask import current_app
from datetime import datetime
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='tasks', lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    goal_id = db.Column(db.Integer, db.ForeignKey(
        'goal.goal_id'), nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'
