from app import db
from app.models import Role


def seed():
    roles = [
        Role(name='Admin'),
        Role(name='Eligibility Manager'),
        Role(name='Eligibility Supervisor'),
        Role(name='Eligibility Specialist'),
        Role(name='Senior Leader')
    ]

    for role in roles:
        db.session.add(role)

    db.session.commit()
