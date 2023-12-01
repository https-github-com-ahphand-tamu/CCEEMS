import logging

from app import create_app
from app.seeds import roles, users, cases

app = create_app()

with app.app_context():
    roles.seed()
    users.seed()
    cases.seed()
    logging.info("Database is seeded!")
