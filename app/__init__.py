import os
import config
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

    configure_logging(app)
    create_config(app)

    app.logger.setLevel(logging.INFO)
    db.init_app(app)

    from app.controllers.user_controller import user_bp
    from app.controllers.new_requests_controller import upload_new_req_bp
    from app.controllers.assign_new_requests import assign
    app.register_blueprint(user_bp)
    app.register_blueprint(upload_new_req_bp)
    app.register_blueprint(assign)

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
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
