import logging

from app import create_app
from app.seeds import roles, users

app = create_app()

with app.app_context():
    roles.seed()
    users.seed()
    logging.info("Database is seeded!")
