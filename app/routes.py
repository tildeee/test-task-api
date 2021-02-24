from flask import Flask, Blueprint, request, jsonify, redirect, url_for
from app.models import ModelEncoder, Task#, Goal
from app import db
from datetime import datetime

import app
import os
import requests

task_page = Blueprint('task_page', __name__)
task_page.json_encoder = ModelEncoder

@task_page.route('/')
def index():
    return {
        "name": "Kaida",
        "message": "Hello, world!"
    }

@task_page.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        return jsonify(Task.query.all())
    elif request.method == 'POST':
        task = Task(**request.json)
        db.session.add(task)
        db.session.commit()

        return jsonify({"task": task})
