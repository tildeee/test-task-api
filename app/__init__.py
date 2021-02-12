from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Task
    with app.app_context():
        db.create_all()

    from .views import simple_page
    app.register_blueprint(simple_page)

    return app
