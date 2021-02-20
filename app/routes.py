from flask import Flask, Blueprint, request, jsonify, redirect, url_for
from app.models import Task
from app import db
from datetime import datetime

task_page = Blueprint('task_page', __name__)


@task_page.route('/')
def index():
    return {
        "name": "Simon Del Rosario",
        "message": "Hi instructors! :)"
    }


def build_dict_from_task(task):
    is_complete = True if task.completed_at else False
    return {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
    }


def build_task_from_json(json):
    return Task(title=json["title"], description=json["description"], completed_at=json["completed_at"])


@task_page.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        results = []
        for task in tasks:
            results.append(build_dict_from_task(task))
        return jsonify(results)
    elif request.method == 'POST':
        new_task = build_task_from_json(request.get_json())

        db.session.add(new_task)
        db.session.commit()

        return {"task": build_dict_from_task(new_task)}


@task_page.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'GET':
        return {"task": build_dict_from_task(task)}
    elif request.method == 'PUT':
        form_data = request.get_json()

        task.title = form_data['title']
        task.description = form_data['description']
        task.completed_at = form_data['completed_at']

        db.session.commit()

        return {"task": build_dict_from_task(task)}
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}


@task_page.route('/tasks/<task_id>/complete', methods=['PATCH'])
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)

    if task.completed_at:
        task.completed_at = None
    else:
        task.completed_at = datetime.utcnow()

    db.session.commit()

    return {"task": build_dict_from_task(task)}



