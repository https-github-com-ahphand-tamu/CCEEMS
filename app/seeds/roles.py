from app import db
from app.models.role import Role


def seed():
    roles = [
        Role(name='admin'),
        Role(name='user'),
    ]

    for role in roles:
        db.session.add(role)

    db.session.commit()
