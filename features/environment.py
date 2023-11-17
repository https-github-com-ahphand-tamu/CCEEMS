import os

from app import db
from features.service import admin_controller_service, update_password_service, \
    new_requests_controller_service
from main import app, login_manager


client = app.test_client()
login_manager.init_app(app)
os.environ['FLASK_ENV'] = 'test'
os.environ['FLASK_DEBUG'] = '1'


def before_feature(context, feature):
    app.logger.info(f"----- Feature: {feature.name} -----")
    context.app = app
    context.client = app.test_client()

    # feature-specific code in service files
    if 'admin-controller' in context.feature.tags:
        admin_controller_service.setup_feature(context, app)
    if 'update-password' in context.feature.tags:
        update_password_service.setup_feature(context, app)
    if 'new-requests' in context.feature.tags:
        new_requests_controller_service.setup_feature(context, app)
    if 'cases-controller' in context.feature.tags:
        cases_controller_service.setup_feature(context, app)

def after_feature(context, feature):
    app.logger.info(f"----- Feature executed: {feature.name} -----")

    # feature-specific code in service files
    if 'admin-controller' in context.feature.tags:
        admin_controller_service.teardown_feature(context, app)
    if 'update-password' in context.feature.tags:
        update_password_service.teardown_feature(context, app)
    if 'new-requests' in context.feature.tags:
        new_requests_controller_service.teardown_feature(context, app)
    if 'cases' in context.feature.tags:
        cases_controller_service.teardown_feature(context, app)

    # If tables are not dropped in above individual teardown, dropping tables here
    with context.app.app_context():
        app.logger.info("Dropping all tables")
        db.drop_all()


def after_all(context):
    with app.app_context():
        db.drop_all()
