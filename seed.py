from app.seeds import roles
from app import create_app

app = create_app()

with app.app_context():
    roles.seed()
