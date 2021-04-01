from flask import request, Blueprint, Response
from flask import Flask, Blueprint, request, jsonify, redirect, url_for, Response
from app.models.task import Task
from app.models.goal import Goal
from app.models.book import Book
from app import db
from datetime import datetime

import os
import requests

task_page = Blueprint('task_page', __name__)


@task_page.route('/')
def index():
    return Response("", 201)


books_bp = Blueprint('books_bp', __name__)


# @books_bp.route('/books', methods=['GET', 'POST'])
# def books():
#     if request.method == 'GET':
#         return {"sup": "hi"}
#     else:
#         response_body = request.get_json()
#         new_book = Book(
#             title=response_body["title"],
#             description=response_body["description"]
#         )

#         db.session.add(new_book)
#         db.session.commit()

#         return Response(f"book_id {new_book.book_id}, title {new_book.title}, description {new_book.description}", status=201)

@books_bp.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        return {"sup": "hi"}
    else:
        response_body = request.get_json()
        new_book = Book(
            title=response_body["title"],
            description=response_body["description"]
        )

        db.session.add(new_book)
        db.session.commit()

        return Response(f"book_id {new_book.book_id}, title {new_book.title}, description {new_book.description}", status=201)


def build_dict_from_task(task):
    is_complete = True if task.completed_at else False
    dict = {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
    }
    if task.goal_id:
        dict["goal_id"] = task.goal_id
    return dict


def build_task_from_json(json):
    return Task(title=json["title"], description=json["description"], completed_at=json["completed_at"])


@task_page.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        if request.args.get("sort") == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        elif request.args.get("sort") == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        else:
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


def post_task_complete_to_slack(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        'Authorization': f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"
    }
    payload = {
        "channel": "secret-simon",
        "text": message
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()


@task_page.route('/tasks/<task_id>/complete', methods=['PATCH'])
def toggle_complete(task_id):
    task = Task.query.get_or_404(task_id)

    if task.completed_at:
        task.completed_at = None
    else:
        task.completed_at = datetime.utcnow()
        slack_response = post_task_complete_to_slack(
            f"Someone just completed the task {task.title}")

    db.session.commit()

    return {"task": build_dict_from_task(task)}


def build_dict_from_goal(goal):
    return {
        "id": goal.goal_id,
        "title": goal.title
    }


def build_goal_from_json(json):
    return Goal(title=json["title"])


@task_page.route('/goals', methods=['GET', 'POST'])
def goals():
    if request.method == 'GET':
        goals = Goal.query.all()
        results = []
        for goal in goals:
            results.append(build_dict_from_goal(goal))
        return jsonify(results)
    elif request.method == 'POST':
        new_goal = build_goal_from_json(request.get_json())

        db.session.add(new_goal)
        db.session.commit()

        return {"task": build_dict_from_goal(new_goal)}


@task_page.route('/goals/<goal_id>', methods=['GET', 'PUT', 'DELETE'])
def goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    if request.method == 'GET':
        return {"goal": build_dict_from_goal(goal)}
    elif request.method == 'PUT':
        form_data = request.get_json()

        goal.title = form_data['title']

        db.session.commit()

        return {"goal": build_dict_from_goal(goal)}
    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}


@task_page.route('/goals/<goal_id>/tasks', methods=['GET', 'POST'])
def goal_tasks(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    if request.method == 'GET':
        tasks = []

        for task in goal.tasks:
            tasks.append(build_dict_from_task(task))

        return {
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks
        }

    if request.method == 'POST':
        goal.tasks = []

        form_data = request.get_json()

        task_ids = form_data['task_ids']

        for task_id in task_ids:
            task = Task.query.get_or_404(task_id)
            goal.tasks.append(task)

        db.session.commit()

        response_task_ids = []
        for task in goal.tasks:
            response_task_ids.append(task.task_id)

        return {
            "id": goal.goal_id,
            "task_ids": response_task_ids
        }
