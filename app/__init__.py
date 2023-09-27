import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.setLevel(logging.INFO)

    db.init_app(app)

    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    return app
