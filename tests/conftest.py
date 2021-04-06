import pytest
from app import create_app
from app.models.task import Task
from app import db


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
        title="Go on my daily walk", description="Notice something new every day", completed_at=None)
    db.session.add(new_task)
    db.session.commit()
