from flask import Flask, Blueprint, request, jsonify, redirect, url_for
from app.models import Task, Goal
from app import db
from datetime import datetime

import os
import requests

task_page = Blueprint('task_page', __name__)
