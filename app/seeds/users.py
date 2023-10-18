from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Role


def seed():
    admin_role = Role.query.filter_by(name="Admin").first()

    user1 = User(name='Test1', email="test1@tamu.edu", role=admin_role)
    user1.password = generate_password_hash("Password@123")
    db.session.add(user1)
    db.session.commit()

    eligibility_supervisor_role = Role.query.filter_by(name="Eligibility Supervisor").first()
    user2 = User(name='Test2', email="test2@tamu.edu", role=eligibility_supervisor_role)
    user2.password = generate_password_hash("Password@456")
    db.session.add(user2)
    db.session.commit()

