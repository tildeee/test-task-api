import tempfile
import pytest
import os
# this import below didn't work until i had an __init__ in here, i knew that bc this error
# ImportError: attempted relative import with no known parent package
from app import create_app
from app.models.task import Task
from app import db

# Need to include that conftest is a Flask Thing


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True})

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def one_task(app):
    new_task = Task(
        title="hi", description="bye", completed_at=None)
    db.session.add(new_task)
    db.session.commit()
