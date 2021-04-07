import pytest
from app import create_app
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_task(app):
    new_task = Task(
        title="Go on my daily walk 🏞", description="Notice something new every day", completed_at=None)
    db.session.add(new_task)
    db.session.commit()


@pytest.fixture
def three_tasks(app):
    db.session.add_all([
        Task(
            title="Water the garden 🌷", description="", completed_at=None),
        Task(
            title="Answer forgotten email 📧", description="", completed_at=None),
        Task(
            title="Pay my outstanding tickets 😭", description="", completed_at=None)
    ])
    db.session.commit()


@pytest.fixture
def completed_task(app):
    new_task = Task(
        title="Go on my daily walk 🏞", description="Notice something new every day", completed_at=datetime.utcnow())
    db.session.add(new_task)
    db.session.commit()


@pytest.fixture
def one_goal(app):
    new_goal = Goal(title="Build a habit of going outside daily")
    db.session.add(new_goal)
    db.session.commit()
