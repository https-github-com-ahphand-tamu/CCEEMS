import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    configure_logging(app)
    create_config(app)

    db.init_app(app)
    configure_session(app)
    register_blueprints(app)

    return app


def create_config(app):
    env = os.environ.get("FLASK_ENV")
    app.logger.info(f"Application environment: {env}")

    if env == 'development':
        app.config.from_object(config.DevelopmentConfig)
    elif env == 'test':
        app.config.from_object(config.TestConfig)
    elif env == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        raise ValueError('Invalid configuration name')


def configure_logging(app):
    app.logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)


def configure_session(app):
    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
    app.config['SESSION_TYPE'] = 'filesystem'
    # Initialize a Flask-Session instance
    Session(app)


def register_blueprints(app):
    from app.controllers.user_controller import user_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.new_requests_controller import upload_new_req_bp
    from app.controllers.assign_new_requests import assign

    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(upload_new_req_bp)
    app.register_blueprint(assign)
