from app import db
from app.seeds import users, roles
from app.models import User


def setup_feature(context, app):
    with app.app_context():
        app.logger.info("Seeding database for update password")
        db.create_all()
        roles.seed()
        users.seed()
        db.session.commit()

    context.response = context.client.post('/user/login', data=dict(
        email="test1@tamu.edu",
        password="Password@123"
    ))
    app.logger.info(f"Login Response: {context.response.status_code}")
    assert context.response.status_code == 302, f"{context.response.status_code} != 302, {context.response.text}"

    context.response = context.client.post('/admin/users', json={
        "name": "Test User3",
        "email": "test3@tamu.edu",
        "role": "Admin"
    })
    app.logger.info(f"Create User Response: {context.response.status_code}")
    assert context.response.status_code == 201, f"{context.response.status_code} != 201, {context.response.text}"

    with app.app_context():
        test_user = db.session.query(User).filter(
            User.email == "test3@tamu.edu").first()
        test_user.verification_code = "abcd-efgh"
    
        db.session.commit()


def teardown_feature(context, app):
    with app.app_context():
        app.logger.info("Dropping all tables in admin controller")
        db.drop_all()
