import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    create_config(app)

    app.logger.setLevel(logging.INFO)
    db.init_app(app)

    from app.controllers.user_controller import user_bp
    from app.controllers.new_requests_controller import upload_new_req_bp
    from app.controllers.list_new_requests import assign
    app.register_blueprint(user_bp)
    app.register_blueprint(upload_new_req_bp)
    app.register_blueprint(assign)

    return app

def create_config(app):
    env = os.environ.get("FLASK_ENV")

    if env == 'development':
        app.config.from_object(config.DevelopmentConfig)
    elif env == 'test':
        app.config.from_object(config.TestConfig)
    elif env == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        raise ValueError('Invalid configuration name')