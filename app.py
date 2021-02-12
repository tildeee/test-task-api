from flask import Flask, request, jsonify, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# This @ line is a decorator. Follow this syntax to make an endpoint.


@app.route('/demo/hello', methods=['GET'])
def hello_world_tacocat():
    # Return our response
    return "Hello, World!"


@app.route('/demo/hello-json', methods=['GET'])
def hello_world_json():
    # jsonify, imported from Flask, let's us jsonify
    return jsonify({
        "Hello": "World"
    })


@app.route('/demo/handles-many-methods', methods=['GET', 'POST', 'DELETE'])
def hello_methods():
    # If we wanted a method that handled many methods,
    # we can use a conditional and read through request
    # request, imported from Flask, gives us info about the request

    if request.method == 'GET':
        return "Nice GET method!"


@app.route('/demo/handles-many-methods', methods=['GET'])
def hello_duplicate_matches():
    return "This will never be seen, because the request matched on the route above."


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def __init__(self, title, description="", completed_at=None):
        self.title = title
        self.description = description
        self.completed_at = completed_at

    def __repr__(self):
        return f'<Task {self.title}>'


# db.drop_all()
db.create_all()
db.session.commit()


@app.route('/')
def index():
    return redirect(url_for('tasks'))


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


@app.route('/tasks', methods=['GET', 'POST'])
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

        return {"tasks": build_dict_from_task(new_task)}


@app.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
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
