from app import db
from app.seeds import users, roles


def setup_feature(context, app):
    with app.app_context():
        app.logger.info("Seeding database in new requests controller")
        db.create_all()
        roles.seed()
        users.seed()
        db.session.commit()

    context.response = context.client.post('/user/login', data=dict(
        email="test1@tamu.edu",
        password="Password@123"
    ))
    app.logger.info(f"Response: {context.response.status_code}")
    assert context.response.status_code == 302, f"{context.response.status_code} != 302, {context.response.text}"


def teardown_feature(context, app):
    with app.app_context():
        app.logger.info("Dropping all tables in new requests controller")
        db.drop_all()
