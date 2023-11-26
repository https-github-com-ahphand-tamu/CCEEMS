from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Role
import logging
import uuid


def seed():
    admin_role = Role.query.filter_by(name="Admin").first()
    logging.info("ADMIN ROLE: " + str(admin_role))
    user1 = User(name='Test1', email="test1@tamu.edu", role=admin_role, verification_code=str(uuid.uuid1()))
    user1.password = generate_password_hash("Password@123")
    db.session.add(user1)
    db.session.commit()

    eligibility_supervisor_role = Role.query.filter_by(
        name="Eligibility Supervisor").first()
    user2 = User(name='Test2', email="test2@tamu.edu",
                 role=eligibility_supervisor_role, verification_code=str(uuid.uuid1()))
    user2.password = generate_password_hash("Password@456")
    user2.verification_code= str(uuid.uuid1())
    db.session.add(user2)
    db.session.commit()

    logging.info("Users seeded")
